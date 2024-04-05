from django.shortcuts import render, redirect
from .forms import index_etlForm
from .models import index_etl
from django.http import HttpResponse
from django.http import JsonResponse

def index_view(request):
    return render(request, 'index.html')

# def add_filter_info(request):
#     if request.method == 'POST':
#         form = index_etlForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # 可以在这里拼凑SQL语句，并将其保存到数据库
#             # 例如：构建SQL语句并执行
#             # sql_statement = "INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...)"
#             return redirect('filterapp:success') # return redirect('success') # 重定向到成功页面
#     else:
#         form = index_etlForm()
#     return render(request, 'add_filter_info.html', {'form': form})

def success(request):
    etl_info_list = index_etl.objects.all()  # 获取所有的过滤器信息

    success_message = request.GET.get('success_message')
    error_message = request.GET.get('error_message')
    return render(request, 'success.html', {'etl_info_list': etl_info_list,'success_message': success_message, 'error_message': error_message})



# def edit_index_etl(request, index_etl_id):
#     try:
#         index_etl_obj = index_etl.objects.get(id=index_etl_id)
#     except index_etl.DoesNotExist:
#         return HttpResponse('Index ETL not found', status=404)
#
#     if request.method == 'POST':
#         new_sql_info = request.POST.get('new_sql_info')
#
#         index_etl_obj.sql_info = new_sql_info
#         index_etl_obj.save()
#
#         # 编辑完成后重定向到编辑页面
#         return redirect('filterapp:success')
#
#     # 如果是 GET 请求，显示编辑页面并传递对象信息
#     return render(request, 'edit_index_etl.html', {'index_etl_obj': index_etl_obj})



def add_or_edit_info(request, index_id=None):
    if index_id:
        is_edit = True
        try:
            index_etl_obj = index_etl.objects.get(id=index_id)
        except index_etl.DoesNotExist:
            return HttpResponseNotFound("指定的指标不存在")
    else:
        is_edit = False
        index_etl_obj = None

    if request.method == 'POST':
        form = index_etlForm(request.POST, instance=index_etl_obj)
        if form.is_valid():
            index_etl_obj = form.save(commit=False)  # 保存表单数据但不提交到数据库
            # 在这里设置其他字段（如果有需要的话）
            index_etl_obj.save()  # 手动提交到数据库
            return redirect('filterapp:success')  # 假设你有一个名为 success 的URL模式
    else:
        form = index_etlForm(instance=index_etl_obj)
    return render(request, 'edit_index.html', {'index_etl_obj': index_etl_obj, 'form': form})


def delete_info(request, index_id):
    error_message = ''  # 初始化 error_message
    success_message = ''  # 初始化 success_message
    try:
        # 根据 index_id 获取要删除的记录
        info = index_etl.objects.get(id=index_id)
        # 删除记录
        info.delete()
        success_message = '删除成功'
    except index_etl.DoesNotExist:
        error_message = '记录不存在'

    return redirect('filterapp:success')