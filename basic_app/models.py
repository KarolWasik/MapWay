from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class AppUsers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    ID_Uzytkownika = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    login = models.CharField(max_length=200, unique=True, default="login")
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)
    avatar = models.IntegerField()

    def __str__(self):
        return self.email
    

class Zgloszenie(models.Model):
    ID_Zgloszenia = models.AutoField(primary_key=True)
    ID_Uzytkownika = models.ForeignKey(AppUsers,null=True, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    typ_zgloszenia = models.IntegerField()
    czas_dodania = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.czas_dodania:
            self.czas_dodania = timezone.now()
        super().save(*args, **kwargs)
