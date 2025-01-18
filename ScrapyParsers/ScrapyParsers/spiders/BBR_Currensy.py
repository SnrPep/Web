import scrapy
import redis
import json


class BbrCurrensySpider(scrapy.Spider):
    name = "BBR_Currensy"
    allowed_domains = ["bbr.ru"]
    start_urls = ["https://bbr.ru/"]
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настроим соединение с Redis
        self.redis_client = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )

        # Проверим подключение
        try:
            self.redis_client.ping()  # Проверяет соединение
            print("Соединение с Redis установлено успешно.")
        except redis.ConnectionError:
            print("Ошибка подключения к Redis.")

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True
            )

        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        if not page:
            self.logger.error("Page not found in meta!")
            return

        self.logger.info(f"Page found: {page.url}")
        # Закрываем страницу после выполнения
        html_content = await page.content()
        await page.close()

        # Передаём контент в Scrapy для дальнейшего парсинга
        response = scrapy.http.HtmlResponse(
            url=response.url, body=html_content, encoding='utf-8'
        )

        new_rates = {}

        for review in response.css(".css-13tn1x7.e314cwc4"):
            exchange_rate = review.css('span.css-11ctayd.exmh6wy0::text').get().replace(",", ".")
            currency_name = review.css('span.css-90qv05.e314cwc2::text').get()

            new_rates[currency_name] = float(exchange_rate)
            try:
                self.redis_client.set("exchange_rates", json.dumps(new_rates))
                print("Данные успешно сохранены в Redis.")
            except redis.RedisError as e:
                print(f"Ошибка при сохранении данных в Redis: {e}")


