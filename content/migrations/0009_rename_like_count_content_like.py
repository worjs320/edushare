# Generated by Django 4.1.2 on 2022-12-10 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0008_remove_content_like_count_content_like_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="content", old_name="like_count", new_name="like",
        ),
    ]
