from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path("register/", views.create_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("home/", views.home, name="home")
]
