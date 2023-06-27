from typing import Any, Dict
from django import forms
from basic_app.models import AppUsers
from django.core import validators


class NewAccount(forms.Form):
    name = forms.CharField(max_length=40, required=True, label="Imie: ")
    last_name = forms.CharField(max_length=40, required=True, label="Nazwisko: ")
    login = forms.CharField(max_length=40, required=True, label="Login: ")
    email  = forms.EmailField(required=True,label="E-mail: ")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło: ")
    submit_password = forms.CharField(widget=forms.PasswordInput(), label="Powtórz hasło: ")
    terms_of_use = forms.BooleanField(label = "Akceptuję warunki i zasady korzystania z aplikacji")
    rodo = forms.BooleanField(label = "Akceptuję politykę prywatności i RODO")


    def clean_submit_password(self):     
        passwordd = self.cleaned_data['password']
        submit_password = self.cleaned_data['submit_password']

        if passwordd != submit_password:
            raise forms.ValidationError("Wprowadzone hasła różnią się!!!")
        if len(passwordd)<6:
            raise forms.ValidationError("Hasło musi mieć minimum 6 znaków!!!")
        return passwordd
    
    def clean_login(self):
        given_login = self.cleaned_data['login']
        login_exists = AppUsers.objects.filter(login=given_login).exists()
        if(len(given_login)<6):
            raise forms.ValidationError("login musi mieć minimum 6 znaków")
        elif(login_exists):
                raise forms.ValidationError("Podany login jest już zajęty! Wprowadź inny login!")

        return given_login
    
    def clean_email(self):
        given_email = self.cleaned_data['email']
        email_exists = AppUsers.objects.filter(email=given_email).exists()
        if(email_exists):
                raise forms.ValidationError("Podany email jest już zajęty! Wprowadź inny email!")

        return given_email
    
    

class SearchCords(forms.Form):
    adress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Szukaj','class' :'form-control', 'id':'search-input'}), label=any, required=False)

class LogIn(forms.Form):
    login = forms.CharField(max_length=40, required=True, label="Login: ")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło: ")
     
    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        correct_login = False
        if login and password:
            try:
                AppUsers.objects.get(login=login)
                correct_login = True
            except AppUsers.DoesNotExist:
                self.add_error('login', "Nie ma użytkownika o podanym loginie")

            if correct_login:
                try:
                    user = AppUsers.objects.get(login=login, password=password)
                except AppUsers.DoesNotExist:
                    self.add_error('password', "Wpisano złe hasło")
        
        return cleaned_data

           
           
     