from django.db import models

from nano_backend.utils.choices import StatusChoice


class Anime(models.Model):
    """
    番剧模型
    """
    title = models.CharField(max_length=100, unique=True, verbose_name='标题')
    title_cn = models.CharField(max_length=100, blank=True, verbose_name='中文标题')

    description = models.TextField(blank=True, null=True, verbose_name='简介')
    cover = models.ImageField(upload_to='animes/cover', verbose_name='封面图片')
    cover_small = models.ImageField(upload_to='animes/cover_small', verbose_name='封面图片(小)')

    place = models.ManyToManyField('places.Place', related_name='anime_related', blank=True, verbose_name='相关地点')

    create_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='anime_create_user',
                                    verbose_name='创建者')
    contributor = models.ManyToManyField('users.User', related_name='anime_contributor', verbose_name='贡献者')

    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.UNPUBLISHED, verbose_name='状态')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'animes'
        db_table = 'tb_anime'
        verbose_name = '番剧信息'
        verbose_name_plural = verbose_name
