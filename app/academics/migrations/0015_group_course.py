# Generated by Django 5.1 on 2025-05-17 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0014_organization_group_organization_subject_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Курс'),
        ),
    ]
