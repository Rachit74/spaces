# Generated by Django 5.1.4 on 2025-01-20 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
        ('todo', '0003_rename_complected_todo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='todo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='todo.todo'),
        ),
    ]
