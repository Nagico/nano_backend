from django.db import models
from django.contrib.auth.models import AbstractUser

from nano_backend.utils.storage import AvatarStorage


class User(AbstractUser):
    """
    用户信息，扩展相关字段
    """

    avatar = models.ImageField(upload_to='avatar', default='avatar/default.jpg', verbose_name='头像',
                               storage=AvatarStorage)

    collection = models.ManyToManyField('animes.Anime', related_name='collection', blank=True, verbose_name='收藏')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
