# Generated by Django 5.1 on 2025-01-08 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_alter_group_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='makalabox_url',
            field=models.URLField(blank=True),
        ),
    ]
