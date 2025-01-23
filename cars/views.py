from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import CarFilter
from django.http import JsonResponse
from .models import Cars

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



# def car_catalog(request):
#     cars = Cars.objects.all()
#     car_filter = CarFilter(request.GET, queryset=cars)
#
#     # Сортировка(НЕ РАБОТАЕТ ПОКА ЧТО!!!)
#     sort_by = request.GET.get('sort', None)
#     if sort_by:
#         cars = car_filter.qs.order_by(sort_by)
#     else:
#         cars = car_filter.qs
#     return render(request, 'car_catalog.html', {'filter': car_filter, 'cars': cars})


def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')  # Получаем ID выбранной марки
    if brand_id:
        # Фильтруем модели, соответствующие выбранной марке
        models = Cars.objects.filter(brand_country_id=brand_id).values_list('model', flat=True).distinct()
        return JsonResponse({'models': list(models)})  # Возвращаем список моделей
    return JsonResponse({'models': []})  # Если марка не выбрана

def car_catalog(request):
    cars = Cars.objects.all()
    car_filter = CarFilter(request.GET, queryset=cars)
    return render(request, 'car_catalog.html', {'filter': car_filter, 'cars': car_filter.qs})