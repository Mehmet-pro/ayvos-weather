# Generated by Django 4.0.3 on 2022-04-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='response_time',
            field=models.IntegerField(),
        ),
    ]
