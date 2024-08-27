# Generated by Django 4.2 on 2024-08-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("med", "0011_remove_services_appointments"),
        ("users", "0007_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="services",
            field=models.ManyToManyField(
                related_name="services", to="med.services", verbose_name="услуги"
            ),
        ),
    ]
