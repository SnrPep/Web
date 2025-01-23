from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('catalog/', views.car_catalog, name='car_catalog'),
    path('get-models/', views.get_models_by_brand, name='get_models'),  # Новый маршрут для AJAX-запроса
]