from django import forms
from .models import index_etl

class index_etlForm(forms.ModelForm):
    class Meta:
        model = index_etl
        fields = ['id','index_no', 'index_name', 'dep_info', 'sql_info']