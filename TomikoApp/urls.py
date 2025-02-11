from django.urls import path
from django.contrib import admin 
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("economy/", views.economy, name="economy"),
    path("catalog/", views.catalog, name="catalog"),
    path("card/", views.card, name="card"),
    path("contacts/", views.contacts, name="contacts"),
    path("politicy/", views.politicy, name="politicy"),
    path("akcii/", views.akcii, name="akcii"),
    path("feedback/", views.feedback_view, name="feedback"),
    path("about/", views.about, name="about"),
    path("404/", views.custom_404, name="404"),
]

