# Generated by Django 4.1 on 2023-05-02 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("basic_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Users",
            new_name="AppUsers",
        ),
    ]