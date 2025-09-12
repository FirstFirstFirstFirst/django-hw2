from django.urls import path
from .views import home, aboutUs

urlpatterns = [
    path('', home, name="home-page"),
    path('about/', aboutUs, name="about-page"),
    path(con)
]
