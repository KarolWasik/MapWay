from django.urls import path
from basic_app import views

app_name = "basic_app"

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("about/", views.about_page, name="about_page"),
    path("dash/", views.dashboard_page, name="dashboard_page"),
    path("map/", views.map_page, name="map_page"),
    path("settings/", views.settings_page, name="settings_page"),
    path("sign/", views.sign_page, name="sign_page"),
    path("", views.main_page, name = "main_page"),
    path("logout/", views.logout_page, name = "logout_page"),
    path("send/", views.send_trafic_data, name = "send_trafic_data"),
    path("route/", views.map_the_route, name = "map_the_route"),
    path("change/", views.change_user_data, name = "change_user_data"),
]