from django import forms
from .models import FilterInfo

class FilterInfoForm(forms.ModelForm):
    class Meta:
        model = FilterInfo
        fields = ['name', 'source_table', 'filter_criteria', 'group_by_field']