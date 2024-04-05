from django.urls import path
from . import views

urlpatterns = [
    path('add_filter_info/', views.add_filter_info, name='add_filter_info'),
    # 可以添加更多的 URL 路由规则
]