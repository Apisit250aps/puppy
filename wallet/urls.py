from django.urls import path
from wallet import views

urlpatterns = [
    path("register", views.register_api, name="register-api"),
    path("login", views.login_api, name="login-api"),
]
