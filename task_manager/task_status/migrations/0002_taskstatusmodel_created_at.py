# Generated by Django 5.0 on 2024-01-23 08:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatusmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]