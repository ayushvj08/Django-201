# Generated by Django 4.0.2 on 2022-03-06 02:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_remove_taskreminder_email_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskreminder',
            name='last_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 5, 8, 15, 27, 192979)),
        ),
    ]
