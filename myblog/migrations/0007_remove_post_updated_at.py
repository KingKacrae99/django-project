# Generated by Django 5.1.2 on 2024-12-16 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myblog", "0006_post_is_trending_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="updated_at",
        ),
    ]
