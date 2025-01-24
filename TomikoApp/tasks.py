from celery import shared_task
from celery import Celery
from TomikoTradeProject.celery import crawl_spider_BBR, crawl_spider_Yandex, crawl_spider_2Gis, crawl_spider_VK, crawl_spider_VL
from cars.models import Cars
from TomikoTradeProject.celery import app
import redis
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from ScrapyParsers.ScrapyParsers.spiders.BBR_Currensy import BbrCurrensySpider


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

app = Celery('tasks')
@app.task
def run_scrapy_BBR():
    crawl_spider_BBR()

@app.task
def run_scrapy_Yandex():
    crawl_spider_Yandex()

@app.task
def run_scrapy_2Gis():
    crawl_spider_2Gis()

@app.task
def run_scrapy_VL():
    crawl_spider_VL()

@app.task
def run_scrapy_VK():
    crawl_spider_VK()


@shared_task
def recalculate_prices():
    """
    Перерасчитывает цены автомобилей: сначала в рубли, затем из рублей в остальные валюты.
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
        prices = {}
        local_price = car.price
        # Определяем страну бренда и локальную валюту
        country = car.brand_country.country.lower()
        if country in ["Китай"]:
            prices["RUB"] = local_price * currency_rates.get("CNY", 1)  # Юань
        elif country in ["Япония"]:
            prices["RUB"] = local_price * currency_rates.get("JPY", 1) # Йена
        elif country in ["США"]:
            prices["RUB"] = local_price * currency_rates.get("USD", 1)  # Доллар
        elif country in ["Европа"]:  # Можно расширить список стран
            prices["RUB"] = local_price * currency_rates.get("EUR", 1)  # Евро
        elif country in ["Корея"]:  # Можно расширить список стран
            prices["RUB"] = local_price * currency_rates.get("CHF", 1) # Вона
        else:
            prices["RUB"] = local_price

        prices = {
            "RUB": prices["RUB"],
            "USD": round(prices["RUB"] / currency_rates.get("USD", 1), 2),
            "EUR": round(prices["RUB"] / currency_rates.get("EUR", 1), 2),
            "CNY": round(prices["RUB"] / currency_rates.get("CNY", 1), 2),
            "JPY": round(prices["RUB"] * 100.0 / currency_rates.get("JPY", 1), 2),
            "CHF": round(prices["RUB"] * 1000.0 / currency_rates.get("CHF", 1), 2),
        }
        
        redis_client.ping()

        # Сохраняем данные в Redis
        try:
            redis_client.set(
                f"car_prices:{car.id}",
                json.dumps(prices)
            )
            print(f"Успешно сохранены данные для машины {car.id}: {prices}")
        except redis.RedisError as e:
            print(f"Ошибка записи в Redis для машины {car.id}: {e}")


