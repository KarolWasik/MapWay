# Generated by Django 4.2.1 on 2023-05-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0019_rename_czas_zgloszenia_zgloszenie_czas_dodania'),
    ]

    operations = [
        migrations.AddField(
            model_name='appusers',
            name='avatar',
            field=models.IntegerField(default=1),
        ),
    ]
