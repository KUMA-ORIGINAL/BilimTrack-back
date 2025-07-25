# Generated by Django 5.1 on 2025-07-19 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_remove_skill_user_remove_user_biography_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=255, verbose_name='Учебное заведение')),
                ('field_of_study', models.CharField(blank=True, max_length=255, null=True, verbose_name='Специальность')),
                ('date', models.CharField(max_length=50, verbose_name='Дата')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Образование',
                'verbose_name_plural': 'Образование',
            },
        ),
    ]
