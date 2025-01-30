from celery import shared_task
from celery import Celery
from decimal import Decimal
from TomikoTradeProject.celery import *
from cars.models import Cars
from TomikoTradeProject.celery import app
import redis
import json

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

app = Celery('tasks')
@app.task
def run_scrapy_all():
    crawl_spiders()

@shared_task
def recalculate_prices():
    """
    Перерасчитывает цены автомобилей и добавляет расчёт пошлины.
    """
    # Получаем курсы валют из Redis
    currency_rates = redis_client.get("exchange_rates")
    if not currency_rates:
        raise ValueError("Курсы валют отсутствуют в Redis!")

    # Преобразуем курсы валют из строки в JSON
    currency_rates = json.loads(currency_rates)

    # Убедимся, что курс рубля задан (должен быть равен 1)
    if "RUB" not in currency_rates:
        currency_rates["RUB"] = 1.0

    # Загружаем автомобили с информацией о бренде
    cars = Cars.objects.select_related("brand_country").all()

    for car in cars:
        car_price_rub = car.price
        # Определяем страну бренда и локальную валюту

        # Расчёт таможенного оформления
        if car_price_rub <= 200_000:
            customs_clearance = 775
        elif car_price_rub <= 450_000:
            customs_clearance = 1550
        elif car_price_rub <= 1_200_000:
            customs_clearance = 3100
        elif car_price_rub <= 2_700_000:
            customs_clearance = 8530
        elif car_price_rub <= 4_200_000:
            customs_clearance = 12000
        elif car_price_rub <= 5_500_000:
            customs_clearance = 15500
        elif car_price_rub <= 7_000_000:
            customs_clearance = 20000
        elif car_price_rub <= 8_000_000:
            customs_clearance = 23000
        elif car_price_rub <= 9_000_000:
            customs_clearance = 25000
        elif car_price_rub <= 10_000_000:
            customs_clearance = 27000
        else:
            customs_clearance = 30000

        # Расчёт единой ставки
        engine_volume = float(car.engine_volume)
        age = 2025 - car.year  # Предполагаем текущий год 2025
        eur_curr = currency_rates["EUR"]
        if age < 3:
            if car_price_rub / eur_curr <= 8500:
                duty_rate = min(0.54 * car_price_rub, 2.5 * engine_volume * eur_curr)
            elif car_price_rub / eur_curr <= 16700:
                duty_rate = min(0.48 * car_price_rub, 3.5 * engine_volume * eur_curr)
            elif car_price_rub / eur_curr <= 42300:
                duty_rate = min(0.48 * car_price_rub, 5.5 * engine_volume * eur_curr)
            elif car_price_rub / eur_curr <= 84500:
                duty_rate = min(0.48 * car_price_rub, 7.5 * engine_volume * eur_curr)
            elif car_price_rub / eur_curr <= 169000:
                duty_rate = min(0.48 * car_price_rub, 15 * engine_volume * eur_curr)
            else:
                duty_rate = min(0.48 * car_price_rub, 20 * engine_volume * eur_curr)
        elif 3 <= age <= 5:
            if engine_volume <= 1000:
                duty_rate = 1.5 * engine_volume * eur_curr
            elif engine_volume <= 1500:
                duty_rate = 1.7 * engine_volume * eur_curr
            elif engine_volume <= 1800:
                duty_rate = 2.5 * engine_volume * eur_curr
            elif engine_volume <= 2300:
                duty_rate = 2.7 * engine_volume * eur_curr
            elif engine_volume <= 3000:
                duty_rate = 3.0 * engine_volume * eur_curr
            else:
                duty_rate = 3.6 * engine_volume * eur_curr
        else:
            if engine_volume <= 1000:
                duty_rate = 3.0 * engine_volume * eur_curr
            elif engine_volume <= 1500:
                duty_rate = 3.2 * engine_volume * eur_curr
            elif engine_volume <= 1800:
                duty_rate = 3.5 * engine_volume * eur_curr
            elif engine_volume <= 2300:
                duty_rate = 4.8 * engine_volume * eur_curr
            elif engine_volume <= 3000:
                duty_rate = 5.0 * engine_volume * eur_curr
            else:
                duty_rate = 5.7 * engine_volume * eur_curr
        # Расчёт утилизационного сбора
        if age < 3:
            utilization_fee = 0.17 * 20000
        else:
            utilization_fee = 0.26 * 20000
        # Итоговая пошлина и итоговая стоимость автомобиля
        total_duty = customs_clearance + duty_rate + utilization_fee
        total_price = car_price_rub + total_duty

        def format_number(n: int) -> str:
            return f"{n:,}".replace(",", " ")
        # Запись данных в словарь
        prices = {
            "RUB": format_number(int(total_price)),
        }
        # Сохраняем данные в Redis
        try:
            redis_client.set(
                f"car_prices:{car.id}",
                json.dumps(prices)
            )
            print(f"Данные для машины {car.id} успешно рассчитаны и сохранены: {prices}")
        except redis.RedisError as e:
            print(f"Ошибка записи данных в Redis для машины {car.id}: {e}")