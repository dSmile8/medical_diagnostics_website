# Generated by Django 5.0 on 2024-08-24 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_doctor",
            field=models.BooleanField(default=False),
        ),
    ]
