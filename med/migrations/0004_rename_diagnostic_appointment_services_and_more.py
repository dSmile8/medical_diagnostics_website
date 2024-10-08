# Generated by Django 4.2 on 2024-08-21 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("med", "0003_alter_doctor_services"),
    ]

    operations = [
        migrations.RenameField(
            model_name="appointment",
            old_name="diagnostic",
            new_name="services",
        ),
        migrations.RemoveField(
            model_name="services",
            name="doctor",
        ),
        migrations.AddField(
            model_name="services",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="image/", verbose_name="иконка"
            ),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="doc_photo/", verbose_name="Фото"
            ),
        ),
        migrations.RemoveField(
            model_name="doctor",
            name="services",
        ),
        migrations.AddField(
            model_name="doctor",
            name="services",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="med.services",
                verbose_name="Услуги",
            ),
        ),
    ]
