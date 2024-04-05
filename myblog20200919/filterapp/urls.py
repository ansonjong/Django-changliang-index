from django.contrib import admin
from django.urls import path
from filterapp import views as filter_views  # 导入你的视图函数
from django.views.generic import TemplateView

app_name = 'filterapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter/index', filter_views.index_view, name='index'),
    # path('filter/add_filter_info/', filter_views.add_filter_info, name='add_filter_info'),  # 指定视图函数
    path('filter/success/', filter_views.success, name='success'),
    # path('delete/<int:filter_id>/', filter_views.delete_filter, name='delete_filter'),
    # path('filter/edit_index_etl/<int:index_etl_id>/', filter_views.edit_index_etl, name='edit_index_etl'),

    # 添加信息的 URL
    path('filter/add/', filter_views.add_or_edit_info, name='add_info'),

    # 编辑信息的 URL，需要传递一个参数 index_id
    path('filter/edit/<int:index_id>/', filter_views.add_or_edit_info, name='edit_info'),

    path('filter/success/<int:index_id>/', filter_views.delete_info, name='delete_info'),

]