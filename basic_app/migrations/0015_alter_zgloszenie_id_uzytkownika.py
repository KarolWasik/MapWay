# Generated by Django 4.1 on 2023-05-21 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("basic_app", "0014_alter_zgloszenie_typ_zgloszenia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="zgloszenie",
            name="ID_Uzytkownika",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="basic_app.appusers",
            ),
        ),
    ]