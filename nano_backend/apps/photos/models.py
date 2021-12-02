from django.db import models

from nano_backend.utils.choices import ImageTypeChoice, StatusChoice


class Photo(models.Model):
    """
    照片存储
    """
    name = models.CharField(max_length=100, verbose_name='照片名称')
    description = models.TextField(blank=True, null=True, verbose_name='照片描述')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    type = models.IntegerField(choices=ImageTypeChoice.choices, default=ImageTypeChoice.REAL, verbose_name='照片类型')

    anime_id = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, related_name='photos', verbose_name='动画')
    place_id = models.ForeignKey('places.Place', on_delete=models.CASCADE, related_name='photos', verbose_name='地点')

    create_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='photo_create_user',
                                    verbose_name='创建者')

    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'photos'
        db_table = 'tb_photo'
        verbose_name = '地点信息'
        verbose_name_plural = verbose_name
