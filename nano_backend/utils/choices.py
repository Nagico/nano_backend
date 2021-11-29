# 枚举类型
from django.db import models


class StatusChoice(models.IntegerChoices):
    """
    状态类型，用于发布状态
    """
    UNPUBLISHED = 0, '未发布'
    PENDING = 1, '待审核'
    PASS = 2, '已发布'
    FAIL = 3, '审核失败'


class ImageTypeChoice(models.IntegerChoices):
    """
    图片类型，用于photo表中的type字段
    """
    REAL = 0, '实景'
    VIRTUAL = 1, '番剧'
    OTHER = 2, '其他'
