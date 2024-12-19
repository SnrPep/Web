from django.shortcuts import render
from django_filters.views import FilterView
from .models import Cars
from .models import Brands
from .filters import CarFilter

def car_list(request):
    # cars = Cars.objects.select_related('brand_country')
    cars = Cars.objects.all()  # Получить все машины из базы
    return render(request, 'car_list.html', {'cars': cars})




def car_catalog(request):
    car_filter = CarFilter(request.GET, queryset=Cars.objects.all())
    return render(request, 'car_catalog.html', {'filter': car_filter})