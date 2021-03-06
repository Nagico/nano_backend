# Generated by Django 3.2.5 on 2021-12-24 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='照片名称')),
                ('description', models.TextField(blank=True, null=True, verbose_name='照片描述')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('type', models.IntegerField(choices=[(0, '实景'), (1, '番剧'), (2, '其他')], default=0, verbose_name='照片类型')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否公开')),
                ('is_approved', models.BooleanField(default=False, verbose_name='是否通过审核')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('anime_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='animes.anime', verbose_name='动画')),
            ],
            options={
                'verbose_name': '照片信息',
                'verbose_name_plural': '照片信息',
                'db_table': 'tb_photo',
            },
        ),
    ]
