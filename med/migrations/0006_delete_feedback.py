# Generated by Django 4.2 on 2024-08-25 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("med", "0005_appointment_result"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Feedback",
        ),
    ]
