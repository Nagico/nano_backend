from django.db import models


class Anime(models.Model):
    """
    Anime模型
    """
    title = models.CharField(max_length=100, unique=True, verbose_name='标题')
    title_cn = models.CharField(max_length=100, blank=True, verbose_name='中文标题')

    description = models.TextField(verbose_name='简介')
    image = models.ImageField(upload_to='animes', verbose_name='图片')

    score_0 = models.IntegerField(default=0, verbose_name='0分')
    score_1 = models.IntegerField(default=0, verbose_name='1分')
    score_2 = models.IntegerField(default=0, verbose_name='2分')
    score_3 = models.IntegerField(default=0, verbose_name='3分')
    score_4 = models.IntegerField(default=0, verbose_name='4分')
    score_5 = models.IntegerField(default=0, verbose_name='5分')

    collection_num = models.IntegerField(default=0, verbose_name='收藏数')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title
