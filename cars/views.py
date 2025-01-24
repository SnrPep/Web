from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import CarFilter
from django.http import JsonResponse
from .models import Cars
import os
import random
from django.conf import settings


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

# def car_catalog(request):
#     cars = Cars.objects.all()
#     car_filter = CarFilter(request.GET, queryset=cars)
#
#     # Получаем параметр сортировки из GET-запроса
#     sort_by = request.GET.get('sort')
#     if sort_by:
#         # Применяем сортировку к отфильтрованным данным
#         cars = car_filter.qs.order_by(sort_by)
#     else:
#         cars = car_filter.qs
#
#     return render(request, 'car_catalog.html', {'filter': car_filter, 'cars': cars})

def car_catalog(request):
    # Путь к папке с изображениями
    image_folder = os.path.join(settings.MEDIA_ROOT, 'Tomiko Trade Photos')

    # Получаем список всех изображений в папке
    image_files = [
        f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))
    ]
    cars = Cars.objects.all()

    # Получаем параметр сортировки из GET-запроса
    sort_param = request.GET.get('sort', None)
    if sort_param:
        cars = cars.order_by(sort_param)

    car_filter = CarFilter(request.GET, queryset=cars)

    for car in car_filter.qs:
        if image_files:
            # Назначаем случайное изображение для записи
            car.random_image = f"/media/Tomiko Trade Photos/{random.choice(image_files)}"
            # print(f"Изображение для {car.model}: {car.random_image}")  # Отладочный вывод
        else:
            car.random_image = None  # Если изображений нет

    return render(request, 'car_catalog.html', {'filter': car_filter, 'cars': car_filter.qs})


def check_images(request):
    # Укажите путь к папке с изображениями
    image_folder = os.path.join(settings.MEDIA_ROOT, 'Tomiko Trade Photos')


    # Проверяем, существует ли папка
    if not os.path.exists(image_folder):
        return JsonResponse({'error': 'Папка с изображениями не найдена'}, status=404)

    # Получаем список файлов в папке
    image_files = [
        f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))
    ]

    # Если изображений нет, сообщаем об этом
    if not image_files:
        return JsonResponse({'message': 'В папке нет изображений'}, status=200)

    # Если изображения найдены, возвращаем их список
    return JsonResponse({'images': os.path.join(settings.MEDIA_URL, 'Tomiko Trade Photos', random.choice(image_files))}, status=200)