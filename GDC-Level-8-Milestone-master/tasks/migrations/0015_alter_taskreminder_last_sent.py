# Generated by Django 4.0.2 on 2022-03-06 05:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_alter_taskreminder_last_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskreminder',
            name='last_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 6, 10, 59, 42, 569116)),
        ),
    ]
