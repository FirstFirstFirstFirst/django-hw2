from django.urls import path

from .views import aboutUs, contact, home, showContact
from django.contrib.auth import views
from django.shortcuts import render, redirect

from myapp.views import userLogin, userRegist, userProfile, editProfile

urlpatterns = [
    path("", home, name="home-page"),
    path("about/", aboutUs, name="about-page"),
    path("contact/", contact, name="contact-page"),
    # path("login/", views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path("login/", userLogin, name='login'),
    path("logout/", views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('showcontact/', showContact, name="showcontact-page"),
    path('register/', userRegist, name="register-page"),
    path('profile', userProfile, name="profile-page"),
    path('editprofile/', editProfile, name="editprofile-page")
    
]
