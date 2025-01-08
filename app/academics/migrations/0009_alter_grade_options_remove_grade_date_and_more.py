# Generated by Django 5.1 on 2025-01-08 03:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0008_grade_comment_alter_grade_grade'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='grade',
            name='date',
        ),
        migrations.AddField(
            model_name='grade',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
