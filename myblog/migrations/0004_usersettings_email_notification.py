# Generated by Django 5.1.2 on 2024-11-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myblog", "0003_alter_post_status_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersettings",
            name="email_notification",
            field=models.BooleanField(default=False),
        ),
    ]
