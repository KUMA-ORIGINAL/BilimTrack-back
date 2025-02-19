# Generated by Django 5.1 on 2025-01-01 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
        ('account', '0005_achievement_rarity_user_achievements_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='academics.group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='achievements',
            field=models.ManyToManyField(blank=True, related_name='users', to='account.achievement'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('mentor', 'Mentor')], default='student', max_length=15),
        ),
    ]
