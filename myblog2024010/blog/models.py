from django.db import models
from django.contrib.auth.models import User

class FilterInfo(models.Model):
    name = models.CharField(max_length=100)
    source_table = models.CharField(max_length=100)  # 添加来源表字段
    filter_criteria = models.TextField()  # 过滤条件
    group_by_field = models.CharField(max_length=100)  # 分组字段