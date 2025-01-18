import scrapy
import redis
import json


class VkClipsSpider(scrapy.Spider):
    name = "VK_clips"
    allowed_domains = ["vk.com"]
    start_urls = ["https://vk.com/clips/tomiko_trade"]

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

        # Закрываем страницу после выполнения
        html_content = await page.content()
        await page.close()

        # Передаём контент в Scrapy для дальнейшего парсинга
        response = scrapy.http.HtmlResponse(
            url=page.url, body=html_content, encoding='utf-8'
        )


        id = 0
        for review in response.css(".vkitGridItem__root--6OepO"):
            new_rewiew = {}
            new_rewiew["Link"] = self.start_urls[0] + review.css('a::attr(href)').get()
            new_rewiew["Prewiew"] = review.css('img.vkuiImageBase__img.vkuiImageBase__img--objectFit-cover::attr(src)').get()

            try:
                self.redis_client.set(f"VK_clip:{id}", json.dumps(new_rewiew))
                print("Данные успешно сохранены в Redis.")
            except redis.RedisError as e:
                print(f"Ошибка при сохранении данных в Redis: {e}")
            id+=1

