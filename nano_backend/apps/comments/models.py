from django.db import models


class Comment(models.Model):
    """
    评论模型
    """
    text = models.TextField(verbose_name='评论内容')
    date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='评论者')
    article = models.ForeignKey('animes.Anime', on_delete=models.CASCADE, verbose_name='评论对象')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='回复')

    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.text[:50]

