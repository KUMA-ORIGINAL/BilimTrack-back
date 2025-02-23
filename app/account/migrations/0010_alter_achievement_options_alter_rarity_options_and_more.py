# Generated by Django 5.1 on 2025-01-26 22:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_skill_tool_alter_user_options_user_biography_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achievement',
            options={'verbose_name': 'Достижение', 'verbose_name_plural': 'Достижения'},
        ),
        migrations.AlterModelOptions(
            name='rarity',
            options={'verbose_name': 'Редкость', 'verbose_name_plural': 'Редкости'},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'verbose_name': 'Технология', 'verbose_name_plural': 'Технологии'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='skills',
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
