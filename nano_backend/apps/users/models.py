from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from nano_backend.utils.fastdfs.fdfs_storage import FastDFSAvatarStorage


class User(AbstractUser):
    """
    用户信息，扩展相关字段
    """

    avatar = models.ImageField(upload_to='avatar', default=settings.DEFAULT_AVATAR_PATH, verbose_name='头像',
                               storage=FastDFSAvatarStorage)
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    collection_anime = models.ManyToManyField('animes.Anime', related_name='collection_user', blank=True,
                                              verbose_name='Anime收藏')
    collection_place = models.ManyToManyField('places.Place', related_name='collection_user', blank=True,
                                              verbose_name='Place收藏')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
