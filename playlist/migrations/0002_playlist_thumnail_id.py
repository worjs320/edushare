# Generated by Django 4.1.3 on 2022-12-13 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='thumnail_id',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
