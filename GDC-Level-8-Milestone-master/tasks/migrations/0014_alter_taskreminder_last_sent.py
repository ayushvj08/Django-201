# Generated by Django 4.0.2 on 2022-03-06 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_alter_taskreminder_last_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskreminder',
            name='last_sent',
            field=models.DateTimeField(null=True),
        ),
    ]
