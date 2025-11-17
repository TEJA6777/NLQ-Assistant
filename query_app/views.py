import os
import re
import pandas as pd
import sqlparse
import logging
import google.generativeai as genai
from django.db import connection, transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from .models import Dataset, Conversation
from .forms import NaturalLanguageQueryForm


load_dotenv()

def configure_genai():
    """Configure Gemini API with the key from environment."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)

# Configure logging
logger = logging.getLogger(__name__)


def get_user_filter(request):
    """Helper function to get user filter for queries."""
    return {'user': request.user} if request.user.is_authenticated else {'user__isnull': True}


def group_datasets_by_name(datasets):
    """
    Group datasets by their base name (without file extension).
    Returns a dictionary where keys are database names and values are lists of datasets.
    Example: {'Student': [dataset1, dataset2], 'College': [dataset3]}
    """
    grouped = {}
    for dataset in datasets:
        # Extract base name (remove file extension and numbers)
        base_name = dataset.name.split('.')[0]  # Remove .csv, .xls, .xlsx
        # Remove trailing numbers and underscores from duplicates
        base_name = base_name.rstrip('_0123456789')
        
        if base_name not in grouped:
            grouped[base_name] = []
        grouped[base_name].append(dataset)
    
    return grouped


def sanitize_table_name(name):
    """Ensure table names are safe for SQLite."""
    name = name.split('.')[0]
    name = re.sub(r'[^\w]', '_', name)
    if name and name[0].isdigit():
        name = '_' + name
    return name.lower()


def clean_sql_response(raw_sql):
    """Clean the SQL response from the model to remove any prefixes or formatting issues."""
    if raw_sql.startswith("```sql"):
        raw_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
    
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "ALTER", "DROP", "CREATE"]
    pattern = r'\b(' + '|'.join(sql_keywords) + r')\b'
    match = re.search(pattern, raw_sql, re.IGNORECASE)
    if match:
        raw_sql = raw_sql[match.start():]
    
    return sqlparse.format(raw_sql, reindent=True, keyword_case='upper')


def execute_sql_statements(sql_statements):
    """Execute multiple SQL statements and return results."""
    cursor = connection.cursor()
    results = []
    columns = []
    total_affected = 0
    is_read_op = False
    
    try:
        with transaction.atomic():
            for stmt in sql_statements:
                stmt = stmt.strip()
                if not stmt:
                    continue
                
                stmt_upper = stmt.upper()
                if stmt_upper.startswith(("SELECT", "PRAGMA")):
                    is_read_op = True
                    cursor.execute(stmt)
                    results = cursor.fetchall()
                    columns = [col[0] for col in cursor.description] if cursor.description else []
                else:
                    cursor.execute(stmt)
                    total_affected += cursor.rowcount
    except Exception as e:
        logger.error(f"SQL Execution Error: {str(e)}")
        raise e
    
    return is_read_op, results, columns, total_affected


def handle_special_queries(query, dataset_id, request):
    """Handle special predefined queries."""
    user_filter = get_user_filter(request)
    
    # Show all databases
    if query.lower() in ["show me all databases", "show all tables", "list all tables", "what databases do you have"]:
        datasets = Dataset.objects.filter(**user_filter)
        if datasets:
            bot_response = "<p><strong>Your uploaded tables:</strong></p><ul>"
            for ds in datasets:
                bot_response += f"<li><strong>{ds.name}</strong> (Table: {ds.table_name})</li>"
            bot_response += "</ul>"
        else:
            bot_response = "<p>You haven't uploaded any tables yet. Upload one to get started!</p>"
        return bot_response, None
    
    # Get current table info
    if query.lower() in ["which data i have uploaded now", "what is the table name", "current table", "which table am i using"]:
        if dataset_id:
            try:
                dataset = Dataset.objects.get(id=dataset_id, **user_filter)
                bot_response = f"<p>Current table: <strong>{dataset.name}</strong> (Internal: {dataset.table_name})</p>"
                return bot_response, dataset
            except Dataset.DoesNotExist:
                pass
        return "<p>No table is currently selected. Please select one from the sidebar.</p>", None
    
    return None, None


def process_file_upload(file, request):
    """Handle file upload and create dataset."""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return None, "Unsupported file format. Please upload CSV or Excel files."
    except Exception as e:
        logger.error(f"File reading error: {str(e)}")
        return None, f"Error reading file: {str(e)}"
    
    table_name = sanitize_table_name(file.name)
    columns = [{"name": col, "type": "TEXT"} for col in df.columns]
    
    try:
        with connection.cursor() as cursor:
            raw_conn = connection.connection
            df.to_sql(table_name, raw_conn, if_exists='replace', index=False)
    except Exception as e:
        logger.error(f"Database save error: {str(e)}")
        return None, f"Error saving to database: {str(e)}"
    
    try:
        dataset = Dataset.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=file.name,
            table_name=table_name,
            columns=columns,
            file=file
        )
        return dataset, None
    except Exception as e:
        logger.error(f"Dataset creation error: {str(e)}")
        return None, f"Error creating dataset: {str(e)}"


def generate_sql_from_query(query, dataset):
    """Generate SQL query from natural language using Gemini AI."""
    try:
        configure_genai()  # Ensure API is configured
        
        # Get all related tables in the same database group
        user_filter = {'user': dataset.user} if dataset.user else {'user__isnull': True}
        base_name = dataset.name.split('.')[0].rstrip('_0123456789')
        related_datasets = Dataset.objects.filter(
            name__startswith=base_name,
            **user_filter
        ).order_by('name')
        
        # Build context about all available tables
        tables_context = "Available tables in this database:\n"
        for ds in related_datasets:
            tables_context += f"- Table: {ds.table_name}\n"
            tables_context += f"  Columns: {', '.join([c['name'] for c in ds.columns])}\n"
        
        sql_prompt = f"""
        You are a SQL expert. Convert the user's natural language request into a VALID SQLite query.
        
        CONTEXT - Database Structure:
        {tables_context}
        
        Primary Table Information:
        - Table name: {dataset.table_name}
        - Columns: {', '.join([c['name'] for c in dataset.columns])}
        
        User Request: "{query}"
        
        IMPORTANT RULES:
        1. ONLY use the tables and columns listed above. Do not invent tables or columns.
        2. For SELECT queries, return the requested data.
        3. For UPDATE, DELETE, INSERT, or ALTER operations, generate appropriate SQL.
        4. Always quote table names and column names with double quotes.
        5. If the user asks to show/display the table, use: SELECT * FROM "{dataset.table_name}" LIMIT 10
        6. For joins, only use tables that exist in the available tables list.
        7. Return ONLY the SQL query - no explanations or markdown.
        8. Ensure the SQL is valid for SQLite.
        """
        
        sql_model = genai.GenerativeModel('gemini-2.0-flash')
        raw_sql = sql_model.generate_content([{"role": "user", "parts": [sql_prompt]}]).text.strip()
        
        return clean_sql_response(raw_sql)
    except Exception as e:
        logger.error(f"SQL generation error: {str(e)}")
        raise e


def generate_chat_response(query, dataset):
    """Generate a friendly chat response using Gemini AI."""
    try:
        configure_genai()  # Ensure API is configured
        
        conversation_prompt = f"""
        You are a friendly Natural Language Query assistant. Answer naturally and helpfully.
        If asked about your purpose, explain: "I help you query your data without writing SQL."
        User: "{query}"
        """
        
        chat_model = genai.GenerativeModel('gemini-2.0-flash')
        response = chat_model.generate_content(
            [{"role": "user", "parts": [conversation_prompt]}]
        ).text.strip()
        
        return f"<p>{response}</p>"
    except Exception as e:
        logger.error(f"Chat generation error: {str(e)}")
        return f"<p>Sorry, I couldn't process that. Error: {str(e)}</p>"


def classify_query(query, dataset):
    """Classify query as SQL or CHAT using Gemini AI."""
    try:
        configure_genai()  # Ensure API is configured
        
        classification_prompt = f"""
        Classify this user message: "{query}"
        - Respond ONLY with "SQL" if it requests to SELECT, INSERT, UPDATE, DELETE, or ALTER data.
        - Respond ONLY with "CHAT" for greetings, general questions, or metadata questions.
        """
        
        classifier = genai.GenerativeModel('gemini-2.0-flash')
        classification = classifier.generate_content(
            [{"role": "user", "parts": [classification_prompt]}]
        ).text.strip().upper()
        
        return classification
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        return "CHAT"


def process_query(request):
    """Main query processing view."""
    if request.method != 'POST':
        return redirect('query_interface')
    
    # Handle file upload
    if 'file' in request.FILES:
        file = request.FILES['file']
        
        # Validate file
        if not file:
            return HttpResponse("No file selected. Please upload a CSV or Excel file.", status=400)
        
        if file.size == 0:
            return HttpResponse("The uploaded file is empty. Please upload a valid file.", status=400)
        
        dataset, error = process_file_upload(file, request)
        
        if error:
            logger.error(f"Upload error: {error}")
            return HttpResponse(f"Upload failed: {error}", status=400)
        
        if not dataset:
            return HttpResponse("Failed to create dataset. Please try again.", status=500)
        
        logger.info(f"Successfully uploaded dataset: {dataset.name} (ID: {dataset.id})")
        return redirect(f'/query/?dataset={dataset.id}&new_upload=true')
    
    # Handle natural language query
    form = NaturalLanguageQueryForm(request.POST)
    if not form.is_valid():
        return redirect('query_interface')
    
    query = form.cleaned_data['query'].strip()
    dataset_id = request.POST.get('dataset')
    user_filter = get_user_filter(request)
    
    if not query:
        return redirect(f'/query/?dataset={dataset_id}' if dataset_id else '/query/')
    
    # Check for special queries first
    special_response, special_dataset = handle_special_queries(query, dataset_id, request)
    if special_response:
        Conversation.objects.create(
            dataset=special_dataset,
            user_query=query,
            sql_query="",
            response=special_response
        )
        return redirect(f'/query/?dataset={dataset_id}' if dataset_id else '/query/')
    
    # Get dataset
    try:
        dataset = Dataset.objects.get(id=dataset_id, **user_filter)
    except Dataset.DoesNotExist:
        error_msg = "<p>Please select a dataset first.</p>"
        Conversation.objects.create(
            dataset_id=dataset_id if dataset_id else None,
            user_query=query,
            sql_query="",
            response=error_msg
        )
        return redirect(f'/query/?dataset={dataset_id}' if dataset_id else '/query/')
    
    # Classify and process query
    classification = classify_query(query, dataset)
    
    if classification == "CHAT":
        bot_response = generate_chat_response(query, dataset)
        Conversation.objects.create(
            dataset=dataset,
            user_query=query,
            sql_query="",
            response=bot_response
        )
    else:  # SQL
        try:
            sql_query = generate_sql_from_query(query, dataset)
            sql_statements = [stmt.strip() for stmt in sql_query.split(';') if stmt.strip()]
            
            is_read_op, results, columns, total_affected = execute_sql_statements(sql_statements)
            
            if is_read_op:
                if results:
                    df = pd.DataFrame(results, columns=columns)
                    html_table = df.to_html(index=False, classes='result-table')
                    bot_response = f"<p>Here's your data:</p>{html_table}"
                else:
                    bot_response = "<p>No results found for your query.</p>"
            else:
                bot_response = f"<p>✓ Operation completed successfully. {total_affected} rows affected.</p>"
            
            Conversation.objects.create(
                dataset=dataset,
                user_query=query,
                sql_query=sql_query,
                response=bot_response
            )
        except Exception as e:
            logger.error(f"Query processing error: {str(e)}")
            error_msg = f"<p>Error: {str(e)}</p>"
            Conversation.objects.create(
                dataset=dataset,
                user_query=query,
                sql_query="",
                response=error_msg
            )
    
    return redirect(f'/query/?dataset={dataset.id}')


def query_interface(request):
    """Display the query chat interface."""
    user_filter = get_user_filter(request)
    datasets = Dataset.objects.filter(**user_filter).order_by('name')
    grouped_datasets = group_datasets_by_name(datasets)
    dataset_id = request.GET.get('dataset')
    selected_dataset = None
    conversations = []
    
    if dataset_id:
        try:
            selected_dataset = Dataset.objects.get(id=dataset_id, **user_filter)
            conversations = Conversation.objects.filter(dataset=selected_dataset).order_by('created_at')
        except Dataset.DoesNotExist:
            selected_dataset = datasets.first() if datasets.exists() else None
    elif datasets.exists():
        selected_dataset = datasets.first()
        conversations = Conversation.objects.filter(dataset=selected_dataset).order_by('created_at')
    
    query_form = NaturalLanguageQueryForm()
    return render(request, 'query.html', {
        'datasets': datasets,
        'grouped_datasets': grouped_datasets,
        'current_dataset': selected_dataset,
        'conversations': conversations,
        'query_form': query_form
    })


def upload_dataset(request):
    """Display the upload dataset page."""
    return render(request, 'upload.html')


def clear_conversation(request):
    """Clear all conversations for a dataset."""
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset')
        user_filter = get_user_filter(request)
        try:
            dataset = Dataset.objects.get(id=dataset_id, **user_filter)
            Conversation.objects.filter(dataset=dataset).delete()
            logger.info(f"Cleared conversations for dataset {dataset_id}")
        except Dataset.DoesNotExist:
            pass
    
    return redirect(f'/query/?dataset={request.POST.get("dataset")}' if request.POST.get('dataset') else '/query/')


def delete_dataset(request):
    """Delete a dataset and all its conversations."""
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id')
        user_filter = get_user_filter(request)
        
        try:
            dataset = Dataset.objects.get(id=dataset_id, **user_filter)
            table_name = dataset.table_name
            
            # Delete conversations first
            Conversation.objects.filter(dataset=dataset).delete()
            
            # Drop the table from database
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
                logger.info(f"Dropped table {table_name}")
            except Exception as e:
                logger.warning(f"Could not drop table {table_name}: {str(e)}")
            
            # Delete the dataset record
            dataset.delete()
            logger.info(f"Deleted dataset {dataset_id}")
            
            return JsonResponse({'success': True, 'message': f'Database "{dataset.name}" deleted successfully'})
        except Dataset.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Database not found'})
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})



def rename_dataset(request):
    """Rename a dataset and its table."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
    dataset_id = request.POST.get('dataset_id')
    new_name = request.POST.get('new_name', '').strip()
    user_filter = get_user_filter(request)
    
    if not new_name:
        return JsonResponse({'success': False, 'message': 'New name cannot be empty'})
    
    try:
        dataset = Dataset.objects.get(id=dataset_id, **user_filter)
        new_table_name = sanitize_table_name(new_name)
        
        with connection.cursor() as cursor:
            cursor.execute(f'ALTER TABLE "{dataset.table_name}" RENAME TO "{new_table_name}"')
        
        dataset.table_name = new_table_name
        dataset.name = new_name
        dataset.save()
        
        logger.info(f"Renamed dataset {dataset_id} to {new_name}")
        return JsonResponse({'success': True, 'message': f'Table renamed to {new_name}'})
    except Exception as e:
        logger.error(f"Rename error: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


# Page Views
def home(request):
    """Home page view."""
    return render(request, 'home.html')


def query_results(request):
    """Results page view."""
    return render(request, 'results.html')


def about(request):
    """About page view."""
    return render(request, 'about.html')


def features(request):
    """Features page view."""
    return render(request, 'features.html')


def contact(request):
    """Contact page view."""
    return render(request, 'contact.html')