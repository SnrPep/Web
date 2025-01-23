from django.urls import path
from django.contrib import admin 
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("economy/", views.economy, name="economy"),
    path("catalog/", views.catalog, name="catalog"),
    path("card/", views.card, name="card"),
    path("contacts/", views.contacts, name="contacts"),
    path("politicy/", views.politicy, name="politicy"),
    path("akcii/", views.akcii, name="akcii"),
    path("feedback/", views.feedback_view, name="feedback"),
]

