# Generated by Django 4.0.2 on 2022-03-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_taskreminder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskreminder',
            name='email_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
