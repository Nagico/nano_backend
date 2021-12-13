from django.db import models


class Recommendation(models.Model):
    """
    首页推荐
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='recommendation/%Y/%m', verbose_name='图片')
    anime = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, verbose_name='动画')
    description = models.CharField(max_length=200, verbose_name='描述')
    score = models.IntegerField(default=0, verbose_name='评分')
    tags = models.ManyToManyField('tags.Tag', verbose_name='标签')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'recommendation'
        db_table = 'tb_recommendation'
        verbose_name = '首页推荐'
        verbose_name_plural = verbose_name
