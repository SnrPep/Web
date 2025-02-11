from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import CarFilter
from django.http import JsonResponse
from .models import Cars
import os
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404


def car_list(request, country=None):
    # Путь к папке с изображениями
    image_folder = os.path.join(settings.MEDIA_ROOT, 'Tomiko Trade Photos')
    image_files = [
        f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))
    ]

    if country:
        cars = Cars.objects.filter(brand_country__country__iexact=country.capitalize())
        popcars = Cars.objects.filter(brand_country__country__iexact=country.capitalize()).order_by('?')[:5]
    else:
        popcars = Cars.objects.all()[:5]
        cars = Cars.objects.all()  # Если страна не указана, показываем все автомобили

    sort_param = request.GET.get('sort', None)
    if sort_param:
        cars = cars.order_by(sort_param)
    else:
        cars = cars.order_by('id')  # Сортировка по умолчанию

    car_filter = CarFilter(request.GET, queryset=cars, country=country)
    if country == "Корея":
        country_name = "Кореи"
        imgFlag = "/static/tomiko/img/icons/korea.svg"
        country_name_eng = ""
    elif country == "Япония":
        country_name = "Японии"
        imgFlag = "/static/tomiko/img/icons/japan.svg"
        country_name_eng = ""
    elif country == "Китай":
        country_name = "Китая"
        imgFlag = "/static/tomiko/img/icons/china.svg"
        country_name_eng = ""
    else:
        country_name = ""
        imgFlag = ""
        country_name_eng = ""

    for car in car_filter.qs:
        if image_files:
            car.random_image = f"/media/Tomiko Trade Photos/{random.choice(image_files)}"
        else:
            car.random_image = None

        # Добавляем базовую цену и цену с пошлинами
        car.price_with_duty = car.get_price_with_duty() # Цена с пошлинами из Redis
        car.price_with_duty2 = car.get_price_with_duty2()

    for car in popcars:
        if image_files:
            car.random_image = f"/media/Tomiko Trade Photos/{random.choice(image_files)}"
        else:
            car.random_image = None

        # Добавляем базовую цену и цену с пошлинами
        car.price_with_duty = car.get_price_with_duty()  # Цена с пошлинами из Redis

    paginator = Paginator(car_filter.qs, 20)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    return render(request, 'car_list.html', {'filter': car_filter, 'cars': cars, 'request': request, 'country': country, 'country_name': country_name, 'imgFlag': imgFlag,'country_name_eng': country_name_eng, 'popular_cars': popcars})


def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')  # Получаем ID выбранной марки
    if brand_id:
        # Фильтруем модели, соответствующие выбранной марке
        models = Cars.objects.filter(brand_country_id=brand_id).values_list('model', flat=True).distinct()
        return JsonResponse({'models': list(models)})  # Возвращаем список моделей
    return JsonResponse({'models': []})  # Если марка не выбрана

def car_catalog(request, country=None):
    # Путь к папке с изображениями
    image_folder = os.path.join(settings.MEDIA_ROOT, 'Tomiko Trade Photos')

    # Получаем список всех изображений в папке
    image_files = [
        f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))
    ]

    if country:
        cars = Cars.objects.filter(brand_country__country__iexact=country)
    else:
        cars = Cars.objects.all()  # Если страна не указана, показываем все автомобили
    # cars = Cars.objects.all()

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

def car_detail(request, country, car_id, price):
    car = get_object_or_404(Cars, id=car_id)

    # Получаем цену с учетом пошлины из Redis
    price_with_duty = car.get_price_with_duty() or car.price  # Если нет данных, используем базовую цену

    # Путь к папке с изображениями
    image_folder = os.path.join(settings.MEDIA_ROOT, 'Tomiko Trade Photos')

    # Получаем список всех изображений в папке
    image_files = [
        f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))
    ]

    # Если страна указана, фильтруем автомобили по стране
    cars = Cars.objects.filter(brand_country__country__iexact=country) if country else Cars.objects.all()

    # Выбираем случайное изображение
    car.random_image = f"/media/Tomiko Trade Photos/{random.choice(image_files)}"

    return render(request, 'car_detail.html', {'car': car, 'price': price_with_duty})