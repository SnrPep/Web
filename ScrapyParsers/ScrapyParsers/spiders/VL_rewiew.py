import scrapy
import redis
import json

class VlRewiewSpider(scrapy.Spider):
    name = "VL_rewiew"
    allowed_domains = ["www.vl.ru"]
    start_urls = ["https://www.vl.ru/tomiko-trade/"]

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

        # Автопрокрутка и клики на "Загрузить ещё комментарии"
        try:
            while True:
                if await page.is_visible("p.loadMoreComments"):
                    await page.click("p.loadMoreComments")
                    await page.wait_for_timeout(2000)  # Ждём 2 секунды для подгрузки данных
                else:
                    break
        except Exception as e:
            self.logger.error(f"Error during autoscrolling: {e}")
        finally:
            # Закрываем страницу после выполнения
            html_content = await page.content()
            await page.close()

            # Передаём контент в Scrapy для дальнейшего парсинга
            response = scrapy.http.HtmlResponse(
                url=page.url, body=html_content, encoding='utf-8'
            )
            new_rewiew = {}
            id = 0
            for review in response.css("#CommentsList .review"):
                try:
                    grade = int(float(review.css(".active::attr(data-value)").get()) * 5.0)
                except:
                    grade = 0

                new_rewiew["name"] = review.css("span.user-name::text").get()
                new_rewiew["date"] = review.css("span.time::text").get().replace('отредактировано ', '')
                new_rewiew["avatar"] = review.css("img::attr(src)").get()
                new_rewiew["grade"] = grade
                try:
                    self.redis_client.set(f"VL_rewiew:{id}", json.dumps(new_rewiew))
                    print("Данные успешно сохранены в Redis.")
                except redis.RedisError as e:
                    print(f"Ошибка при сохранении данных в Redis: {e}")


