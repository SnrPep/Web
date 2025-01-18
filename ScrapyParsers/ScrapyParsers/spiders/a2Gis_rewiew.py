import scrapy
import redis
import json

class A2gisRewiewSpider(scrapy.Spider):
    name = "2Gis_rewiew"
    allowed_domains = ["2gis.ru"]
    start_urls = ["https://2gis.ru/vladivostok/firm/70000001067259118/tab/reviews"]

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
        await page.wait_for_timeout(2000)
        html_content = await page.content()
        await page.close()

        # Передаём контент в Scrapy для дальнейшего парсинга
        response = scrapy.http.HtmlResponse(
            url=page.url, body=html_content, encoding='utf-8'
        )

        reviews = {}  # Список для хранения всех отзывов
        id = 0
        for review in response.css("._1k5soqfl"):
            try:
                grade = len(review.css("._1fkin5c").css("span"))
            except:
                grade = 0
            try:
                text = review.css("._1dk5lq4::attr(style)").get()
                start = text.find('url(\"")') + len('url(\"")')
                end = text.find('\"); border-radius: 0px')
                avatar = text[start:end]
            except:
                avatar = None

            new_review = {
                "name": review.css("span._16s5yj36::text").get(),
                "date": review.css("._139ll30::text").get().replace(', отредактирован', ''),
                "avatar": avatar,
                "grade": grade,
            }

            try:
                self.redis_client.set(f"2Gis_review:{id}", json.dumps(new_review))
                print("Данные успешно сохранены в Redis.")
            except redis.RedisError as e:
                print(f"Ошибка при сохранении данных в Redis: {e}")
            id += 1
        # Сохраняем все отзывы в Redis

