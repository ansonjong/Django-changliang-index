from django import forms
from .models import index_etl
from .models import TableInfo

class index_etlForm(forms.ModelForm):
    class Meta:
        model = index_etl
        fields = ['id','index_no', 'index_name', 'dep_info', 'sql_info']


class InputForm(forms.Form):
    input1 = forms.CharField(label='Input 1', max_length=100)
    input2 = forms.CharField(label='Input 2', max_length=100)
    input3 = forms.CharField(label='Input 3', max_length=100)
    input4 = forms.CharField(label='Input 4', max_length=100)
    textarea = forms.CharField(label='Textarea', widget=forms.Textarea)
    checkbox = forms.BooleanField(label='Checkbox')
    dropdown = forms.ChoiceField(label='Dropdown', choices=[('option1', 'Option 1'), ('option2', 'Option 2')])

class MySQLDDLForm(forms.Form):
    ddl_statement = forms.CharField(widget=forms.Textarea)