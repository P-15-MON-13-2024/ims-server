# forms.py
from django import forms

class SapienUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file')
