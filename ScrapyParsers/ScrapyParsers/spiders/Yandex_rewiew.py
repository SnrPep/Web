import scrapy
import redis
import json

class YandexRewiewSpider(scrapy.Spider):
    name = "Yandex_rewiew"
    allowed_domains = ["yandex.ru"]
    start_urls = ["https://yandex.ru/maps/org/tomiko_trade/126455019912/reviews/?ll=131.922567%2C43.127157&z=16"]

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
        # Эмулируем действия пользователя

        html_content = await page.content()
        await page.close()

        # Передаём контент в Scrapy для дальнейшего парсинга
        response = scrapy.http.HtmlResponse(
            url=page.url, body=html_content, encoding='utf-8'
        )
        new_rewiew = {}
        id = 0
        for review in response.css(".business-reviews-card-view__review"):
            try:
                name = review.css("a.business-review-view__link").css("span::text").get()
            except:
                name = None
            try:
                date = review.css("span.business-review-view__date::text").css("span").get().replace(', отредактирован',
                                                                                                     '')
            except:
                date = None
            try:
                grade = len(review.css("span.business-rating-badge-view__star._full").getall())
            except:
                grade = 0
            try:
                avatar = review.css("a.business-review-view__user-icon::attr(href)").get()
            except:
                avatar = None
            new_rewiew["name"] = name
            new_rewiew["date"] = date
            new_rewiew["avatar"] = avatar
            new_rewiew["grade"] = grade
            try:
                self.redis_client.set(f"Yandex_review:{id}", json.dumps(new_rewiew))
                print("Данные успешно сохранены в Redis.")
            except redis.RedisError as e:
                print(f"Ошибка при сохранении данных в Redis: {e}")
            id+=1

