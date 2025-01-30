import os
from celery import Celery
from celery.schedules import crontab
from ScrapyParsers.ScrapyParsers.spiders.BBR_Currensy import BbrCurrensySpider
from ScrapyParsers.ScrapyParsers.spiders.a2Gis_rewiew import A2gisRewiewSpider
from ScrapyParsers.ScrapyParsers.spiders.VK_clips import VkClipsSpider
from ScrapyParsers.ScrapyParsers.spiders.VL_rewiew import VlRewiewSpider
from ScrapyParsers.ScrapyParsers.spiders.Yandex_rewiew import YandexRewiewSpider

broker_connection_retry_on_startup = True

# Установка переменной окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TomikoTradeProject.settings')

app = Celery('TomikoApp')

# Загрузка настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task
def crawl_spiders():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'BOT_NAME': 'scrapybot',
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(BbrCurrensySpider)
    process.crawl(VkClipsSpider)
    process.crawl(YandexRewiewSpider)
    process.crawl(VlRewiewSpider)
    process.crawl(A2gisRewiewSpider)

    process.start()

app.conf.beat_schedule = {
    "parse-every-day": {
        "task": "TomikoApp.tasks.run_scrapy_all",
        'schedule': crontab(hour=9, minute=33),  # Выполнение каждый день в 00:00
        'options': {
            'replace_existing': True  # Заменяет существующую задачу при запуске
        }
    },
    "recalculate-every-day": {
        "task": "TomikoApp.tasks.recalculate_prices",
        'schedule': crontab(hour=9, minute=35),  # Выполнение каждый день в 00:02 - 2 минуты достаточно для того, чтобы отпарсить всё необходимое
        'options': {
            'replace_existing': True  # Заменяет существующую задачу при запуске
        }
    },
}