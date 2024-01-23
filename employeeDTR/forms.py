# forms.py
from django import forms

class UploadFileForm(forms.Form):
    excelFile = forms.FileField(label='Choose an Excel file', widget=forms.FileInput(attrs={'accept': '.xls, .xlsx'}))
