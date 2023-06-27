# Generated by Django 4.1 on 2023-05-20 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("basic_app", "0009_remove_appusers_id_appusers_id_uzytkownika"),
    ]

    operations = [
        migrations.CreateModel(
            name="Zgloszenie",
            fields=[
                ("ID_Zgloszenia", models.AutoField(primary_key=True, serialize=False)),
                ("x", models.IntegerField()),
                ("y", models.IntegerField()),
                ("Czas_zgloszenia", models.DateField()),
                (
                    "ID_Uzytkownika",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="basic_app.appusers",
                    ),
                ),
            ],
        ),
    ]
