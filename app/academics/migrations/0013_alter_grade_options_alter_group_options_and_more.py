# Generated by Django 5.1 on 2025-01-28 08:41

import django.db.models.deletion
import imagekit.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0012_grade_date_alter_grade_grade'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ('-created_at',), 'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-points'], 'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name'], 'verbose_name': 'Предмет', 'verbose_name_plural': 'Предметы'},
        ),
        migrations.AlterField(
            model_name='grade',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.IntegerField(choices=[(0, 'Не был'), (1, 'Оценка 1'), (2, 'Оценка 2'), (3, 'Оценка 3'), (4, 'Оценка 4'), (5, 'Оценка 5'), (6, 'Оценка 6'), (7, 'Оценка 7'), (8, 'Оценка 8'), (9, 'Оценка 9'), (10, 'Оценка 10')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.subject', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='group',
            name='contract',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='contracts/%Y', verbose_name='Контракт'),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='points',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Очки'),
        ),
        migrations.AlterField(
            model_name='group',
            name='rules',
            field=models.JSONField(blank=True, help_text='Правила для группы', null=True, verbose_name='Правила'),
        ),
        migrations.AlterField(
            model_name='group',
            name='subjects',
            field=models.ManyToManyField(related_name='groups', to='academics.subject', verbose_name='Предметы'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='makalabox_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на Makalabox'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='subjects/%Y', verbose_name='Фото'),
        ),
    ]
