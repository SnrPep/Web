from django.shortcuts import render
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .models import Cars
from .models import Brands
from .filters import CarFilter

def car_list(request):
    cars_list = Cars.objects.all()
    paginator = Paginator(cars_list, 20)  # Показывать 50 карточек на странице
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    return render(request, 'car_list.html', {'cars': cars})
    # cars = Cars.objects.all()  # Получить все машины из базы
    # return render(request, 'car_list.html', {'cars': cars})




def car_catalog(request):
    cars = Cars.objects.all()
    car_filter = CarFilter(request.GET, queryset=cars)

    # Сортировка(НЕ РАБОТАЕТ ПОКА ЧТО!!!)
    sort_by = request.GET.get('sort', None)
    if sort_by:
        cars = car_filter.qs.order_by(sort_by)
    else:
        cars = car_filter.qs
    return render(request, 'car_catalog.html', {'filter': car_filter, 'cars': cars})