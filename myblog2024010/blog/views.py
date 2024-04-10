from django.shortcuts import render, redirect
from .forms import FilterInfoForm
from .models import FilterInfo

def add_filter_info(request):
    if request.method == 'POST':
        form = FilterInfoForm(request.POST)
        if form.is_valid():
            filter_info = form.save()
            # 在这里可以根据用户输入构建SQL语句并执行
            # 例如：构建SQL语句并执行
            # sql_statement = f"SELECT * FROM {filter_info.source_table} WHERE {filter_info.filter_criteria} GROUP BY {filter_info.group_by_field}"
            return redirect('success')  # 重定向到成功页面
    else:
        form = FilterInfoForm()
    return render(request, 'add_filter_info.html', {'form': form})