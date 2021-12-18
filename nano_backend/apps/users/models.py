from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from nano_backend.utils.fastdfs.fdfs_storage import FastDFSAvatarStorage


class UserAnimeCollection(models.Model):
    """
    用户收藏的Anime
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    anime = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, verbose_name='Anime')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user_anime_collection'
        verbose_name = '用户收藏的Anime'
        verbose_name_plural = verbose_name


class UserAnimeHistory(models.Model):
    """
    用户Anime历史
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    anime = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, verbose_name='Anime')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user_anime_history'
        verbose_name = '用户Anime历史'
        verbose_name_plural = verbose_name


class UserPlaceCollection(models.Model):
    """
    用户收藏的Place
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    place = models.ForeignKey('places.Place', on_delete=models.CASCADE, verbose_name='Place')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user_place_collection'
        verbose_name = '用户收藏的Place'
        verbose_name_plural = verbose_name


class User(AbstractUser):
    """
    用户信息，扩展相关字段
    """

    avatar = models.ImageField(upload_to='avatar', default=settings.DEFAULT_AVATAR_PATH, verbose_name='头像',
                               storage=FastDFSAvatarStorage)
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    collection_anime = models.ManyToManyField('animes.Anime', related_name='collection_user',
                                              through='users.UserAnimeCollection', blank=True, verbose_name='Anime收藏')
    history_anime = models.ManyToManyField('animes.Anime', related_name='history_user',
                                           through='users.UserAnimeHistory', blank=True, verbose_name='Anime历史')
    collection_place = models.ManyToManyField('places.Place', related_name='collection_user',
                                              through='users.UserPlaceCollection', blank=True, verbose_name='Place收藏')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


