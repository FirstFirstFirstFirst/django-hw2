from django.urls import path

from .views import aboutUs, contact, home
from django.contrib.auth import views

urlpatterns = [
    path("", home, name="home-page"),
    path("about/", aboutUs, name="about-page"),
    path("contact/", contact, name="contact-page"),
    path("login/", views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path("logout/", views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout')
]
