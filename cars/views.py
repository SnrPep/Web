from django.shortcuts import render
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .models import Cars
from .models import Brands
from .filters import CarFilter

def car_list(request):
    car_filter = CarFilter(request.GET, queryset=Cars.objects.all())
    paginator = Paginator(car_filter.qs, 20)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    return render(request, 'car_list.html', {'filter': car_filter, 'cars': cars, 'request': request})

    # cars_list = Cars.objects.all()
    # paginator = Paginator(cars_list, 20)  # Показывать 20 карточек на странице
    # page_number = request.GET.get('page')
    # cars = paginator.get_page(page_number)
    # return render(request, 'car_list.html', {'cars': cars})



def car_catalog(request):
    car_filter = CarFilter(request.GET, queryset=Cars.objects.all())
    return render(request, 'car_catalog.html', {'filter': car_filter})