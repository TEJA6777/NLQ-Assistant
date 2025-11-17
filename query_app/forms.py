from django import forms


class DatasetUploadForm(forms.Form):
    """Form for uploading dataset files."""
    file = forms.FileField(
        label='Dataset (CSV/Excel)',
        help_text='Upload a CSV or Excel file (supports .csv, .xls, .xlsx)',
        widget=forms.FileInput(attrs={
            'accept': '.csv, .xls, .xlsx',
            'class': 'form-control'
        })
    )

    def clean_file(self):
        """Validate file type."""
        file = self.cleaned_data.get('file')
        if file:
            valid_extensions = ['.csv', '.xls', '.xlsx']
            if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError(
                    f"Unsupported file format. Please upload CSV or Excel files."
                )
        return file


class NaturalLanguageQueryForm(forms.Form):
    """Form for natural language queries."""
    query = forms.CharField(
        label='Your Question',
        required=True,
        min_length=1,
        max_length=1000,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g.: Show me all customers from New York',
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        help_text='Ask a question about your data in natural language'
    )

    def clean_query(self):
        """Validate and clean query."""
        query = self.cleaned_data.get('query', '').strip()
        if not query:
            raise forms.ValidationError("Please enter a question.")
        if len(query) > 1000:
            raise forms.ValidationError("Question is too long. Maximum 1000 characters.")
        return query
