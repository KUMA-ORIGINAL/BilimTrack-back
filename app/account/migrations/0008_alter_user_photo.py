# Generated by Django 5.1 on 2025-01-02 20:13

import imagekit.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_achievements_count_user_points_user_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='user_photos/%Y/%m'),
        ),
    ]
