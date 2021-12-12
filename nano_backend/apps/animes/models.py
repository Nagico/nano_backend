from django.db import models


class Anime(models.Model):
    """
    番剧模型
    """
    title = models.CharField(max_length=100, unique=True, verbose_name='标题')
    title_cn = models.CharField(max_length=100, blank=True, verbose_name='中文标题')

    description = models.TextField(blank=True, null=True, verbose_name='简介')
    cover = models.ImageField(upload_to='animes/cover', verbose_name='封面图片')
    cover_medium = models.ImageField(upload_to='animes/cover_medium', verbose_name='中等尺寸封面图片')
    cover_small = models.ImageField(upload_to='animes/cover_small', verbose_name='封面图片(正)')

    tags = models.ManyToManyField('tags.Tag', blank=True, verbose_name='标签')

    epi_num = models.IntegerField(default=1, verbose_name='集数')
    director = models.ManyToManyField('staffs.Staff', related_name='director', blank=True, verbose_name='导演')
    original = models.ManyToManyField('staffs.Staff', related_name='original', blank=True, verbose_name='原作')
    script = models.ManyToManyField('staffs.Staff', related_name='script', blank=True, verbose_name='脚本')
    storyboard = models.ManyToManyField('staffs.Staff', related_name='storyboard', blank=True, verbose_name='分镜')
    actor = models.ManyToManyField('staffs.Staff', related_name='actor', blank=True, verbose_name='演出')
    music = models.ManyToManyField('staffs.Staff', related_name='music', blank=True, verbose_name='音乐')
    producer = models.ManyToManyField('staffs.Staff', related_name='producer', blank=True, verbose_name='制作')
    website = models.CharField(max_length=200, blank=True, null=True, verbose_name='官网')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='制片国家')
    air_date = models.DateField(blank=True, null=True, verbose_name='首播日期')

    create_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='anime_create_user',
                                    verbose_name='创建者')
    contributor = models.ManyToManyField('users.User', related_name='anime_contributor', verbose_name='贡献者')

    collection_num = models.IntegerField(default=0, verbose_name='收藏数')

    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    is_approved = models.BooleanField(default=False, verbose_name='是否通过审核')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'animes'
        db_table = 'tb_anime'
        verbose_name = '番剧信息'
        verbose_name_plural = verbose_name


class AnimeAlias(models.Model):
    """
    作品别名
    """
    title = models.CharField(max_length=100, unique=True, verbose_name='标题')
    anime = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, related_name='alias', verbose_name='作品')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'animes'
        db_table = 'tb_anime_alias'
        verbose_name = '作品别名'
        verbose_name_plural = verbose_name
