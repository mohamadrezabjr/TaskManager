# Generated by Django 5.1.7 on 2025-03-10 21:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_project_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='created',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
