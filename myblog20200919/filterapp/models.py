from django.db import models
from django.contrib.auth.models import User

class index_etl(models.Model):
    id = models.AutoField(primary_key=True)
    index_no = models.CharField(max_length=100)
    index_name = models.CharField(max_length=100)  # 添加来源表字段
    dep_info = models.CharField(max_length=100)  # 分组字段
    sql_info = models.TextField()  # 过滤条件
    # 添加自增长的ID字段
