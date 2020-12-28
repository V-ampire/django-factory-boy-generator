# Generated by Django 3.1.4 on 2020-12-17 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0002_auto_20201217_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='timestamp',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]