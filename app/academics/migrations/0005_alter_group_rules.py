# Generated by Django 5.1 on 2025-01-02 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_alter_group_options_alter_group_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='rules',
            field=models.JSONField(blank=True, help_text='Правила для группы', null=True),
        ),
    ]
