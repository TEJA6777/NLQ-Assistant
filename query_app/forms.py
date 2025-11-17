from django import forms

class DatasetUploadForm(forms.Form):
    file = forms.FileField(
        label='Dataset (CSV/Excel)',
        help_text='Upload a CSV or Excel file.'
    )

class NaturalLanguageQueryForm(forms.Form):
    query = forms.CharField(
        label='Your Question',
        widget=forms.TextInput(attrs={'placeholder': 'E.g.: Show me customers from New York'})
    )
