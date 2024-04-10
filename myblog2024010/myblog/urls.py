from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter/', include('filterapp.urls')),
    # 包含你的应用程序 URL 配置
]