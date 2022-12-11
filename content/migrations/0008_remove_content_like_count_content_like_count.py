# Generated by Django 4.1.2 on 2022-12-10 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("content", "0007_note_title"),
    ]

    operations = [
        migrations.RemoveField(model_name="content", name="like_count",),
        migrations.AddField(
            model_name="content",
            name="like_count",
            field=models.ManyToManyField(
                blank=True, related_name="like_count", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
