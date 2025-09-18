from django.urls import path
from .views import home, aboutUs, contact

urlpatterns = [
    path('', home, name="home-page"),
    path('about/', aboutUs, name="about-page"),
    path('contact/', contact, name="contact-page")
]
