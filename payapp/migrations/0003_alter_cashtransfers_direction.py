# Generated by Django 4.1.7 on 2023-05-03 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_cashtransfers_cashrequests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashtransfers',
            name='direction',
            field=models.CharField(max_length=20),
        ),
    ]
