from django.db import models


class Place(models.Model):
    """
    地点模型
    """
    name = models.CharField(max_length=100, verbose_name='地点名称')
    address = models.CharField(max_length=200, default='', verbose_name='地址')
    latitude = models.FloatField(default=0, verbose_name='纬度')
    longitude = models.FloatField(default=0, verbose_name='经度')
    description = models.TextField(blank=True, null=True,  verbose_name='地点描述')

    anime_id = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, related_name='places', verbose_name='动画')

    create_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='place_create_user',
                                    verbose_name='创建者')
    contributor = models.ManyToManyField('users.User', related_name='place_contributor', verbose_name='贡献者')

    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')

    collection_num = models.IntegerField(default=0, verbose_name='收藏数')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'places'
        db_table = 'tb_places'
        verbose_name = '地点信息'
        verbose_name_plural = verbose_name
