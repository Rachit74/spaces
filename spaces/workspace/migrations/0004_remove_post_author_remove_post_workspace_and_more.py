# Generated by Django 5.1.4 on 2025-01-17 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_workspacerequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='workspace',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
