import os
from celery import Celery
from ScrapyParsers.ScrapyParsers.spiders.BBR_Currensy import BbrCurrensySpider
from ScrapyParsers.ScrapyParsers.spiders.a2Gis_rewiew import A2gisRewiewSpider
from ScrapyParsers.ScrapyParsers.spiders.VK_clips import VkClipsSpider
from ScrapyParsers.ScrapyParsers.spiders.VL_rewiew import VlRewiewSpider
from ScrapyParsers.ScrapyParsers.spiders.Yandex_rewiew import YandexRewiewSpider


# Установка переменной окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TomikoTradeProject.settings')

app = Celery('TomikoApp')

# Загрузка настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task
def crawl_spider_BBR():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'BOT_NAME': 'scrapybot',
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(BbrCurrensySpider)
    process.start()
@app.task
def crawl_spider_2Gis():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'BOT_NAME': 'scrapybot',
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(A2gisRewiewSpider)
    process.start()
@app.task
def crawl_spider_VL():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'BOT_NAME': 'scrapybot',
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(VlRewiewSpider)
    process.start()
@app.task
def crawl_spider_Yandex():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'BOT_NAME': 'scrapybot',
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(YandexRewiewSpider)
    process.start()
@app.task
def crawl_spider_VK():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(VkClipsSpider)
    process.start()


