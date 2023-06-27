from django.shortcuts import render
from basic_app import forms
from basic_app.models import AppUsers, Zgloszenie
from geopy.geocoders import Nominatim
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.utils import timezone
import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



# Create your views here.
def get_coordinates(city, street):
    geolocator = Nominatim(user_agent="my-app") # utwórz obiekt geolokalizatora
    location = geolocator.geocode(f"{street}, {city}") # pobierz współrzędne geograficzne
    try:
        return location.latitude, location.longitude
    except AttributeError:
        return False

def main_page(request):
    user = request.user
    if user.is_authenticated:
        app_user = AppUsers.objects.get(user=user)
        avatar = str(app_user.avatar)
        context = {
            'user': user,
            'avatar': avatar,
        }
    else:
        context = {
            'user': user,
        }
    return render(request, 'basic_app/main.html', context)

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login

def login_page(request):
    if request.method == "POST":
        login_form = forms.LogIn(request.POST)
        if login_form.is_valid():
            # Sprawdź poprawność formularza i uzyskaj dostęp do danych
            login_value = login_form.cleaned_data['login']
            password = login_form.cleaned_data['password']

            # Uwierzytelnij użytkownika
            user = authenticate(request, username=login_value, password=password)
            if user is not None:
                # Logowanie powiodło się
                login(request, user)
                next_page = reverse('basic_app:map_page')
                return redirect(next_page)
            else:
                # Logowanie nie powiodło się
                # Dodaj odpowiedni komunikat błędu
                login_form.add_error(None, "Nieprawidłowy login lub hasło.")
    else:
        login_form = forms.LogIn()

    return render(request, 'basic_app/logowanie.html', {'login_form': login_form})

def about_page(request):
    user = request.user
    if user.is_authenticated:
        app_user = AppUsers.objects.get(user=user)
        avatar = str(app_user.avatar)
        context = {
            'user': user,
            'avatar': avatar,
        }
    else:
        context = {
            'user': user,
        }
    return render(request, 'basic_app/about.html', context)

@login_required(login_url='basic_app:login_page')
def dashboard_page(request):
    user = request.user
    if user.is_authenticated:
        app_user = AppUsers.objects.get(user=user)
        name = app_user.name
    return render(request, 'basic_app/dashboard.html', {'name':name})

@login_required(login_url='basic_app:login_page')
def map_page(request):
    current_time = timezone.now()
    two_minutes_ago = current_time - timezone.timedelta(minutes=120)
    Zgloszenie.objects.filter(czas_dodania__lte=two_minutes_ago).delete()
    print(two_minutes_ago, "     ", Zgloszenie)

    
    utrudnienia = Zgloszenie.objects.filter(typ_zgloszenia=1).values_list('x', 'y', 'czas_dodania', 'ID_Uzytkownika__login','typ_zgloszenia')
    utrudnienia = [(float(x), float(y), czas_dodania.strftime('%Y-%m-%dT%H:%M:%S'), login, typ) for x, y, czas_dodania, login, typ in utrudnienia]


    kontrole = Zgloszenie.objects.filter(typ_zgloszenia=2).values_list('x', 'y', 'czas_dodania', 'ID_Uzytkownika__login', 'typ_zgloszenia')
    kontrole = [(float(x), float(y), czas_dodania.strftime('%Y-%m-%dT%H:%M:%S'), login, typ) for x, y, czas_dodania, login, typ in kontrole]

    fotoradary = Zgloszenie.objects.filter(typ_zgloszenia=3).values_list('x', 'y', 'czas_dodania', 'ID_Uzytkownika__login', 'typ_zgloszenia')
    fotoradary = [(float(x), float(y), czas_dodania.strftime('%Y-%m-%dT%H:%M:%S'), login, typ) for x, y, czas_dodania, login, typ in fotoradary]
    
    user = request.user
    app_user = AppUsers.objects.get(user=user)
    avatar = str(app_user.avatar)

    form = forms.SearchCords()
    cordx = str(50.041088)
    cordy = str(21.999156)
    zoom = 13
    search_pin=False
    if(request.method =="POST"):
        form = forms.SearchCords(request.POST)
        if form.is_valid():
            search_pin = True
            adress = str(form.cleaned_data['adress']).split(",")
            if len(str(adress[0])) >1:
                try:
                    cords = get_coordinates(adress[0],adress[1])
                except IndexError:
                    cords = get_coordinates(adress[0],'')
                if cords == False:
                    messages.error(request, 'nie znaleziono adresu')
                    next_page = reverse('basic_app:map_page')
                    return redirect(next_page)
                else:   
                    cordx = cords[0]
                    cordy = cords[1]
                zoom = 16
                print(form.cleaned_data['adress'])
    context = {
            'form':form,
            'cordx':cordx,
            'cordy':cordy,
            'zoom':zoom,
            'search_pin':search_pin,
            'utrudnienia': utrudnienia,
            'fotoradary':fotoradary,
            'kontrole':kontrole,
            'avatar':avatar,
        }
    return render(request, 'basic_app/mapa.html', context)



@login_required(login_url='basic_app:login_page')
def settings_page(request):
    user = request.user
    if user.is_authenticated:
        app_user = AppUsers.objects.get(user=user)
        # Tutaj masz dostęp do pól modelu AppUsers dla zalogowanego użytkownika
        name = app_user.name
        last_name = app_user.last_name
        login = app_user.login
        email = app_user.email
        user_id = app_user.ID_Uzytkownika
        avatar = str(app_user.avatar)

        password = app_user.password[0]+ "****" + app_user.password[-1]

        context = {
            'name': name,
            'last_name': last_name,
            'login': login,
            'email': email,
            'id' : user_id,
            'password': password,
            'avatar':avatar,
        }
    return render(request, 'basic_app/ustawienia.html', context)

def sign_page(request):
    form = forms.NewAccount()
    if(request.method =="POST"):
        form = forms.NewAccount(request.POST)
        if form.is_valid():
            # przypisanie loginu i hasła do zmiennych
            login=form.cleaned_data['login']
            password=form.cleaned_data['password']
            # utworzenie modelu newUser
            newUser = AppUsers()
            # przypisanie danych do modelu
            newUser.name = form.cleaned_data['name']
            newUser.last_name=form.cleaned_data['last_name']
            newUser.email=form.cleaned_data['email']
            newUser.login = login
            newUser.password = password
            newUser.avatar = random.randint(1, 9)
            #przypisanie danych do autoryzacji podczas logowania
            user = User.objects.create_user(username=login, password=password)
            newUser.user = user
            # zapisanie danych w bazie
            newUser.save()
            user.save()
            return login_page(request)
        else:
            print("error form fdafas")
            
    return render(request, 'basic_app/rejestracja.html',{'form':form})


def logout_page(request):
    logout(request)
    next_page = reverse('basic_app:main_page')
    return redirect(next_page)

def send_trafic_data(request):
    if request.method == 'POST':
        user = request.user
        app_user = AppUsers.objects.get(user=user)
        report_trafic = Zgloszenie()
        data = json.loads(request.body)
        x = data.get('variable1')
        y = data.get('variable2')
        typ_zgloszenia = data.get('variable3')

        report_trafic.ID_Uzytkownika = app_user
        report_trafic.x = x
        report_trafic.y = y
        report_trafic.typ_zgloszenia = typ_zgloszenia
        report_trafic.save()
        print(x, "  " , y , "   " , typ_zgloszenia)

        # Wykonaj dalsze czynności z otrzymanymi danymi

        return JsonResponse({'message': 'Dane odebrane poprawnie.'})

    return JsonResponse({'message': 'Metoda nieobsługiwana.'}, status=405)


def map_the_route(request):
    if request.method == 'POST':
        # Odczytaj dane przesłane z frontendu
        adress1 = request.POST.get('variable1')
        adress2 = request.POST.get('variable2')

        # Wykonaj dowolne operacje na przesłanych danych
        adress1 = str(adress1).split(",")
        adress2 = str(adress2).split(",")
        if len(str(adress1[0])) >1:
            try:
                cords = get_coordinates(adress1[0],adress1[1])
            except IndexError:
                cords = get_coordinates(adress1[0],'')
            if cords == False:
                messages.error(request, 'nie znaleziono adresu')
                next_page = reverse('basic_app:map_page')
                return redirect(next_page)
            else:   
                x1 = cords[0]
                y1 = cords[1]
            print(adress1)

        if len(str(adress2[0])) >1:
            try:
                cords = get_coordinates(adress2[0],adress2[1])
            except IndexError:
                cords = get_coordinates(adress2[0],'')
            if cords == False:
                messages.error(request, 'nie znaleziono adresu')
                next_page = reverse('basic_app:map_page')
                return redirect(next_page)
            else:   
                x2 = cords[0]
                y2 = cords[1]
            print(adress2)
        # np. obliczenia, przetwarzanie itp.

        # Przygotuj odpowiedź w formie słownika
        response_data = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

        # Zwróć odpowiedź jako JSON
        return JsonResponse(response_data)
    
def change_user_data(request):
    message = 'dane zostały zmienione'
    if request.method == 'POST':
        user = request.user
        app_user = AppUsers.objects.get(user=user)
        data = json.loads(request.body)
        new_data = data.get('variable1')
        changed_field = data.get('variable2')
        if changed_field == 1:
            if len(str(new_data))>0:
                app_user.name = new_data
                app_user.save()
        if changed_field == 2:
            login_exists = AppUsers.objects.filter(login=new_data).exists()
            if login_exists:
                message = "login jest zajęty"
            elif len(str(new_data))<6:
                message = "podany login jest zbyt krótki"
            else:
                user.username = str(new_data)
                app_user.login = str(new_data)
                user.save()
                app_user.save()
        if changed_field == 3:
            if len(str(new_data))>0:
                app_user.last_name = new_data
                app_user.save()
        if changed_field == 4:
            try:
                validate_email(new_data)
                is_valid = True
            except ValidationError:
                is_valid = False
            if is_valid:
                mail_exists = AppUsers.objects.filter(email=new_data).exists()
                if mail_exists:
                    message = "podany email jest zajęty"
                else:
                    app_user.email = new_data
                    app_user.save()
            else:
                message = "wprowadzono błędny adres email"
        if changed_field == 5:
            if len(str(new_data))<6:
                message = "nowe hasło musi mieć minimum 6 znaków"
            else:
                user.set_password(new_data)
                app_user.password = new_data
                user.save()
                app_user.save()
    if len(str(new_data))<1:
        message = "nie wprowadzono danych do zmiany"
    response_data = {
            'message': message
        }
    return JsonResponse(response_data)
