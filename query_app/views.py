import os
import re
import pandas as pd
import sqlparse
import google.generativeai as genai
from django.db import connection, transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from .models import Dataset, Conversation
from .forms import NaturalLanguageQueryForm


load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


def sanitize_table_name(name):
    """Ensure table names are safe for SQLite."""
    # Remove file extension
    name = name.split('.')[0]
    # Replace spaces and special chars with underscores
    name = re.sub(r'[^\w]', '_', name)
    # Ensure it doesn't start with a number
    if name[0].isdigit():
        name = '_' + name
    return name.lower()


def clean_sql_response(raw_sql):
    """Clean the SQL response from the model to remove any prefixes or formatting issues."""
    # Remove markdown code blocks
    if raw_sql.startswith("```sql"):
        raw_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
    
    # Remove any prefixes before SQL keywords
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
                    columns = [col[0] for col in cursor.description]
                else:
                    cursor.execute(stmt)
                    total_affected += cursor.rowcount
    except Exception as e:
        raise e
    
    return is_read_op, results, columns, total_affected


def process_query(request):
    if request.method == 'POST':

        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    return HttpResponse("Unsupported file format. Please upload CSV or Excel files.", status=400)
            except Exception as e:
                return HttpResponse(f"Error reading file: {str(e)}", status=400)
            
            table_name = sanitize_table_name(file.name)
            columns = [{"name": col, "type": "TEXT"} for col in df.columns]
            
            try:
                with connection.cursor() as cursor:
                    raw_conn = connection.connection
                    df.to_sql(table_name, raw_conn, if_exists='replace', index=False)
            except Exception as e:
                return HttpResponse(f"Error saving to database: {str(e)}", status=500)
            
            dataset = Dataset.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=file.name,
                table_name=table_name,
                columns=columns,
                file=file
            )
            
            return redirect(f'/query/?dataset={dataset.id}&new_upload=true')
        

        else:
            form = NaturalLanguageQueryForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                dataset_id = request.POST.get('dataset')
                new_upload = request.GET.get('new_upload', 'false').lower() == 'true'
                

                if query.lower() in ["show me all databases", "show all tables", "list all tables", "what databases do you have"]:
                    user_datasets = Dataset.objects.filter(
                        user=request.user if request.user.is_authenticated else None
                    )
                    if user_datasets:
                        bot_response = "<p>Here are your uploaded tables:</p><ul>"
                        for dataset in user_datasets:
                            bot_response += f"<li>{dataset.name} (Table: {dataset.table_name})</li>"
                        bot_response += "</ul>"
                    else:
                        bot_response = "<p>You haven't uploaded any tables yet.</p>"
                    Conversation.objects.create(
                        dataset=None,
                        user_query=query,
                        sql_query="",
                        response=bot_response
                    )
                    return redirect('/query/')
                
                if query.lower() in ["which data i have uploaded now", "what is the table name", "current table"]:
                    dataset = Dataset.objects.filter(id=dataset_id).first()
                    if dataset:
                        bot_response = f"<p>Your current uploaded table is: <b>{dataset.name}</b> (Internal name: {dataset.table_name})</p>"
                    else:
                        bot_response = "<p>No table is currently selected.</p>"
                    Conversation.objects.create(
                        dataset_id=dataset_id if dataset_id else None,
                        user_query=query,
                        sql_query="",
                        response=bot_response
                    )
                    return redirect(f'/query/?dataset={dataset_id}' if dataset_id else '/query/')
                

                if query.lower().startswith("change table name to") or query.lower().startswith("rename table to"):
                    new_name = query.lower().replace("change table name to", "").replace("rename table to", "").strip()
                    dataset = Dataset.objects.filter(id=dataset_id).first()
                    if dataset:
                        new_table_name = sanitize_table_name(new_name)
                        
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f'ALTER TABLE "{dataset.table_name}" RENAME TO "{new_table_name}"')
                            
                            dataset.table_name = new_table_name
                            dataset.name = new_name
                            dataset.save()
                            
                            bot_response = f"<p>Table renamed to: <b>{new_name}</b> (Internal name: {new_table_name})</p>"
                        except Exception as e:
                            bot_response = f"<p>Error renaming table: {str(e)}</p>"
                    else:
                        bot_response = "<p>No table is currently selected.</p>"
                    
                    Conversation.objects.create(
                        dataset=dataset,
                        user_query=query,
                        sql_query="",
                        response=bot_response
                    )
                    return redirect(f'/query/?dataset={dataset.id}')
                

                table_request_pattern = r'(show me|display|list|get)\s+(the\s+)?(.+?)\s+(table|data)'
                match = re.search(table_request_pattern, query.lower())
                if match:
                    requested_table = match.group(3).strip()
                    try:
                        requested_dataset = Dataset.objects.get(
                            name__iexact=requested_table,
                            user=request.user if request.user.is_authenticated else None
                        )
                        sql_query = f'SELECT * FROM "{requested_dataset.table_name}" LIMIT 10'
                        cursor = connection.cursor()
                        cursor.execute(sql_query)
                        results = cursor.fetchall()
                        columns = [col[0] for col in cursor.description]
                        
                        if results:
                            df = pd.DataFrame(results, columns=columns)
                            html_table = df.to_html(index=False, classes='result-table')
                            bot_response = f"<p>Here's the data from table '{requested_dataset.name}':</p>{html_table}"
                        else:
                            bot_response = f"<p>No data found in table '{requested_dataset.name}'.</p>"
                        
                        Conversation.objects.create(
                            dataset=requested_dataset,
                            user_query=query,
                            sql_query=sql_query,
                            response=bot_response
                        )
                        return redirect(f'/query/?dataset={requested_dataset.id}')
                    except Dataset.DoesNotExist:
                        pass
                

                try:
                    dataset = Dataset.objects.get(
                        id=dataset_id,
                        user=request.user if request.user.is_authenticated else None
                    )
                    
                    classification_prompt = f"""
                    Classify this user message: "{query}"
                    - Respond ONLY with "SQL" if it is a request to SELECT, INSERT, UPDATE, DELETE, or ALTER table data.
                    - Respond ONLY with "CHAT" for greetings, assistant info, or metadata questions (like table names).
                    """
                    classifier = genai.GenerativeModel('gemini-2.0-flash')
                    classification = classifier.generate_content(
                        [{"role": "user", "parts": [classification_prompt]}]
                    ).text.strip().upper()
                    

                    if classification == "CHAT":
                        conversation_prompt = f"""
                        You are a friendly assistant. Answer naturally.
                        If asked "what do you do?", respond:
                        "I'm a Natural Language Query assistant. You can upload tables like '{dataset.name}' and ask me to view, update, delete, or modify data without writing SQL."
                        User: "{query}"
                        """
                        chat_model = genai.GenerativeModel('gemini-2.0-flash')
                        chat_response = chat_model.generate_content(
                            [{"role": "user", "parts": [conversation_prompt]}]
                        ).text.strip()
                        Conversation.objects.create(
                            dataset=dataset,
                            user_query=query,
                            sql_query="",
                            response=f"<p>{chat_response}</p>"
                        )
                        return redirect(f'/query/?dataset={dataset.id}')
                    

                    else:
                        sql_prompt = f"""
                        Convert this user request into a VALID SQLite SQL query.
                        - Table name: {dataset.table_name}
                        - Columns: {', '.join([c['name'] for c in dataset.columns])}
                        - User request: "{query}"
                        
                        Important notes:
                        1. For SELECT queries, return the data as requested.
                        2. For UPDATE, DELETE, INSERT, or ALTER operations, generate the appropriate SQL.
                        3. Return ONLY the SQL query (no explanations, no extra text).
                        4. Ensure the SQL is valid for SQLite.
                        5. Always quote table names and column names with double quotes to handle special characters.
                        6. If the user asks for the complete table, generate: SELECT * FROM "{dataset.table_name}"
                        7. If the user asks to show the table, generate: SELECT * FROM "{dataset.table_name}" LIMIT 10
                        8. For complex operations like adding a column and then updating it, generate separate SQL statements separated by semicolons.
                        9. Do not include any text before the SQL statement.
                        """
                        sql_model = genai.GenerativeModel('gemini-2.0-flash')
                        raw_sql = sql_model.generate_content([{"role": "user", "parts": [sql_prompt]}]).text.strip()
                        
                        sql_query = clean_sql_response(raw_sql)
                        
                        sql_statements = [stmt.strip() for stmt in sql_query.split(';') if stmt.strip()]
                        
                        try:
                            is_read_op, results, columns, total_affected = execute_sql_statements(sql_statements)
                            
                            if is_read_op:
                                if results:
                                    df = pd.DataFrame(results, columns=columns)
                                    html_table = df.to_html(index=False, classes='result-table')
                                    bot_response = f"<p>Here's the data based on your query:</p>{html_table}"
                                else:
                                    bot_response = "<p>No results found for your query.</p>"
                            else:
                                bot_response = f"<p>Operation executed successfully. {total_affected} rows affected in total.</p>"
                            
                            Conversation.objects.create(
                                dataset=dataset,
                                user_query=query,
                                sql_query=sql_query,
                                response=bot_response
                            )
                            return redirect(f'/query/?dataset={dataset.id}')
                            
                        except Exception as e:
                            error_message = f"<p>SQL Error: {str(e)}</p>"
                            error_message += f"<p>Generated SQL: {sql_query}</p>"
                            Conversation.objects.create(
                                dataset=dataset,
                                user_query=query,
                                sql_query=sql_query,
                                response=error_message
                            )
                            return redirect(f'/query/?dataset={dataset.id}')
                
                except Dataset.DoesNotExist:
                    return HttpResponse("Please upload a dataset first.", status=400)
                except Exception as e:
                    error_message = f"<p>Something went wrong: {str(e)}</p>"
                    Conversation.objects.create(
                        dataset_id=dataset_id if dataset_id else None,
                        user_query=query,
                        sql_query="",
                        response=error_message
                    )
                    return redirect(f'/query/?dataset={dataset_id}' if dataset_id else '/query/')
    
    return redirect('query_interface')


def query_interface(request):
    datasets = Dataset.objects.filter(
        user=request.user if request.user.is_authenticated else None
    )
    dataset_id = request.GET.get('dataset')
    selected_dataset = None
    conversations = []
    new_upload = request.GET.get('new_upload', 'false').lower() == 'true'
    
    if dataset_id:
        try:
            selected_dataset = Dataset.objects.get(id=dataset_id, user=request.user if request.user.is_authenticated else None)
            conversations = Conversation.objects.filter(dataset=selected_dataset).order_by('created_at')
        except Dataset.DoesNotExist:
            selected_dataset = None
    elif datasets.exists():
        selected_dataset = datasets.first()
        conversations = Conversation.objects.filter(dataset=selected_dataset).order_by('created_at')
    
    query_form = NaturalLanguageQueryForm()
    return render(request, 'query.html', {
        'datasets': datasets,
        'selected_dataset': selected_dataset,
        'conversations': conversations,
        'query_form': query_form,
        'new_upload': new_upload
    })

# ---------------------------
# Clear Conversation View
# ---------------------------
def clear_conversation(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset')
        Conversation.objects.filter(dataset_id=dataset_id).delete()
        return redirect(f'/query/?dataset={dataset_id}')
    return redirect('query_interface')

# ---------------------------
# Rename Dataset View
# ---------------------------
def rename_dataset(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id')
        new_name = request.POST.get('new_name')
        try:
            dataset = Dataset.objects.get(
                id=dataset_id,
                user=request.user if request.user.is_authenticated else None
            )
            # Sanitize the new table name
            new_table_name = sanitize_table_name(new_name)
            
            # Rename the table in the database
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER TABLE "{dataset.table_name}" RENAME TO "{new_table_name}"')
            
            # Update the dataset record
            dataset.table_name = new_table_name
            dataset.name = new_name
            dataset.save()
            
            return JsonResponse({'success': True, 'message': f'Table renamed to {new_name}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error renaming table: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# ---------------------------
# Home & Results Views
# ---------------------------
def home(request):
    return render(request, 'index.html')

def query_results(request):
    return render(request, 'results.html')