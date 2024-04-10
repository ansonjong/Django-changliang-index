from django.shortcuts import render, redirect
from .forms import index_etlForm
from .forms import InputForm
from .models import index_etl
import sqlparse
from .forms import MySQLDDLForm
from .models import TableInfo

from .models import col_type_mapping
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.http import urlencode
import re

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


def extract_table_info(sql):
    table_name_match = re.search(r'CREATE TABLE `?(\w+)`?', sql)
    table_name = table_name_match.group(1) if table_name_match else ''

    fields_match = re.findall(r'`?(\w+)`?\s+(\w+)(?:\((\d+)\))?(?:\s+(PRIMARY KEY|FOREIGN KEY|UNIQUE|NOT NULL|AUTO_INCREMENT))?', sql)

    print("Fields matched:", fields_match)  # Add this line for debugging

    # Filter out items where name is "CREATE"
    table_info = [{'name': name, 'type': type_, 'length': length if length else '', 'constraint': constraint if constraint else ''}
                  for name, type_, length, constraint in fields_match if name.lower() != 'create']

    print("Table info:", table_info)  # Add this line for debugging

    return table_name, table_info

def display_table_info(request):
    mysql_sql = ''
    source_system = ''
    partition_info = ''
    table_info = []
    # primary_keys = []
    table_name = ''
    col_map = [
        ["Data 1", "Data 2"],
        ["VARCHAR", "string"],
        ["int", "bigint"],
        ["number", "bigint"]
    ]

    if request.method == 'POST':
        mysql_sql = request.POST.get('mysql_sql', '')
        partition_info = request.POST.get('partition_info', '')
        table_location = request.POST.get('table_location', '')
        # primary_keys = request.POST.getlist('primary_key[]')
        source_system = request.POST.get('source_system', '')
    else:
        mysql_sql = 'CREATE TABLE example_table (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), age INT)'

    table_name, table_info = extract_table_info(mysql_sql)

    # col_map_dict = {item[0].lower(): item[1] for item in col_map[1:]}  # 忽略第一行，因为第一行是标题行
    col_map_dict = {}
    for item in col_map[1:]:
        # 将每个元素的两个值都转换为小写
        col_map_dict[item[0].lower()] = item[1].lower()

    # 根据 table_info 中的 type 列去匹配 col_map 中的第一列，然后将对应的第二列内容添加到 table_info 中的一个新列 hive_col
    for col_info in table_info:
        type_lower = col_info['type'].lower()
        col_info['hive_col'] = col_map_dict.get(type_lower, '')

    return render(request, 'con_index.html',
                  {'mysql_sql': mysql_sql, 'table_name': table_name, 'table_info': table_info,'col_map': col_map,'source_system': source_system,'partition_info': partition_info})

def submit_table_info(request):
    primary_keys = []
    if request.method == 'POST':
        # 处理表单提交数据的逻辑...
        imary_keys = request.POST.getlist('primary_key[]')
        # 处理完毕后返回一个响应
        return render(request, 'con_index.html',{'primary_keys': primary_keys})  # 渲染一个成功提交的页面

    else:
        return HttpResponse('只允许 POST 请求！')

def about(request):
    col_Data = [
        ["Data 1", "Data 2"],
        ["Another Data 1", "Another Data 2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["A其他1", "A其他2"],
        ["VARCHAR", "string"]
    ]
    return render(request, 'about.html',{'col_Data': col_Data})

def a_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # 处理表单提交的数据
            data = urlencode({
                'input1': form.cleaned_data['input1'],
                'input2': form.cleaned_data['input2'],
                'input3': form.cleaned_data['input3'],
                'input4': form.cleaned_data['input4'],
                'textarea': form.cleaned_data['textarea'],
                'checkbox': form.cleaned_data['checkbox'],
                'dropdown': form.cleaned_data['dropdown'],
            })
            redirect_url = redirect('filterapp:b_view').url + '?' + data
            return redirect(redirect_url)
    else:
        form = InputForm()
    return render(request, 'a.html', {'form': form})

def b_view(request):
    data = {
        'input1': request.GET.get('input1', ''),
        'input2': request.GET.get('input2', ''),
        'input3': request.GET.get('input3', ''),
        'input4': request.GET.get('input4', ''),
        'textarea': request.GET.get('textarea', ''),
        'checkbox': request.GET.get('checkbox', ''),
        'dropdown': request.GET.get('dropdown', ''),
    }
    return render(request, 'b.html', {'data': data})


def parse_ddl(ddl_statement):
    # 修改正则表达式以匹配可能在反引号中的表名
    table_name_match = re.search(r'CREATE TABLE(?: IF NOT EXISTS)? `?(\w+)`?', ddl_statement)
    table_name = table_name_match.group(1) if table_name_match else ''

    # 调整字段匹配的正则表达式，确保不匹配 IF NOT EXISTS
    fields_match = re.findall(
        r'`?(\w+)`?\s+(\w+)(?:\((\d+)\))?(?:\s+(PRIMARY KEY|FOREIGN KEY|UNIQUE|NOT NULL|AUTO_INCREMENT|IF NOT EXISTS))?', ddl_statement)

    # 过滤掉字段名为 'create' 的情况，以避免识别错误
    columns = [{'name': name, 'type': type_, 'length': int(length) if length else None,
                'constraint': constraint if constraint else ''}
               for name, type_, length, constraint in fields_match if name.lower() != 'create']

    return table_name, columns

def process_ddl(request):
    col_map = {
        "varchar": "nvarchar2",
        "int": "bigint",
        "number": "bigint"
    }

    if request.method == 'POST':
        source_system = request.POST.get('source_system', '') # 获取来源系统
        operation = request.POST.get('operation', '') # 获取操作类型（增量或全量）
        form = MySQLDDLForm(request.POST)
        if form.is_valid():
            ddl_statement = form.cleaned_data['ddl_statement']
            table_name, columns = parse_ddl(ddl_statement)
            if table_name and columns:
                # 清空旧数据
                TableInfo.objects.filter(table_name=table_name).delete()
                for column in columns:
                    type_lower = column['type'].lower()
                    # 如果找到了匹配的键，返回对应的值，否则返回空字符串
                    hive_col = col_map.get(type_lower, '')
                    if hive_col and column.get('length'):
                        hive_col += f"({column['length']})"
                    TableInfo.objects.create(
                        table_name=table_name,
                        column_name=column['name'],
                        column_type=column['type'],
                        column_length=column.get('length', ''),
                        hive_column_type=hive_col
                    )
                # 从数据库中获取字段信息并拼接 Hive 的建表语句
                table_info_objects = TableInfo.objects.filter(table_name=table_name)
                hive_columns = [f"{table_info.column_name} {table_info.hive_column_type}" for table_info in table_info_objects]
                d_table_name=f"tgf_dcl.d_{source_system}_{table_name}"
                o_table_name = f"tgf_ods.o_{source_system}_{table_name}"
                d_ddl = f"CREATE TABLE {d_table_name} (\n" + ",\n".join(hive_columns) + "\n,record_fin nvarchar2(32),\netl_timestamp timestamp,\netl_dt date)"
                o_ddl = f"CREATE TABLE {o_table_name} (\n" + ",\n".join(hive_columns) + "\n,record_fin nvarchar2(32),\nstart_dat nvarchar2(32),\nend_date nvarchar2(32),\netl_timestamp timestamp,\netl_dt date)"
                col_info = table_info_objects

                dml_col = [f"{table_info.column_name} " for table_info in table_info_objects]

                obs_info = f"ak'' \nsk '' \npath='obs/xxx/xxx/xx/';"
                d_et = f"dorp table {d_table_name}_et;\ncreate table {d_table_name}_et (\n" + ",\n".join(dml_col) +"\n);"
                d_insert = f"insert into {d_table_name} \nselect \n"+ ",\n".join(dml_col) +",\nrecord_fin ,\netl_timestamp ,\netl_dt"
                d_drop= f"from {d_table_name} ;\ndrop table {d_table_name}_ex; \n 分析语句;"
                d_dml = f"{d_et} \n {obs_info} \n {d_insert} \n {d_drop}"
                return render(request, 'hive_table.html', {'d_ddl': d_ddl,'o_ddl': o_ddl,'col_info': col_info,'d_dml': d_dml})
    else:
        form = MySQLDDLForm()
    return render(request, 'process_ddl.html', {'form': form})

def submit_primary_info(request):
    primary_keys = []
    if request.method == 'POST':
        # 处理表单提交数据的逻辑...
        imary_keys = request.POST.getlist('primary_key[]')
        # 处理完毕后返回一个响应
        return render(request, 'hive_table.html',{'primary_keys': primary_keys})  # 渲染一个成功提交的页面

    else:
        return HttpResponse('只允许 POST 请求！')