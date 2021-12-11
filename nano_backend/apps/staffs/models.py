from django.db import models


class Staff(models.Model):
    """
    staff模型
    """
    name = models.CharField(max_length=100, verbose_name='姓名')
    avatar = models.ImageField(upload_to='animes/staff/avatar', blank=True, null=True, verbose_name='头像')
    description = models.TextField(blank=True, null=True, verbose_name='简介')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'staffs'
        db_table = 'tb_staff'
        verbose_name = 'staff信息'
        verbose_name_plural = verbose_name
