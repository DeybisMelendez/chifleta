# Generated by Django 5.1.2 on 2024-11-06 02:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='posts.post'),
        ),
    ]
