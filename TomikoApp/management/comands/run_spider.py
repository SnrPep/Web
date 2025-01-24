from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from parsers.parsers.spiders.a2Gis_rewiew import A2gisRewiewSpider
from parsers.parsers.spiders.VL_rewiew import VlRewiewSpider
from parsers.parsers.spiders.Yandex_rewiew import YandexRewiewSpider
from parsers.parsers.spiders.BBR_Currensy import BbrCurrensySpider
from parsers.parsers.spiders.VK_clips import VkClipsSpider

SPIDERS = {
    "A2gisRewiewSpider": A2gisRewiewSpider,
    "VlRewiewSpider": VlRewiewSpider,
    "YandexRewiewSpider": YandexRewiewSpider,
    "BbrCurrensySpider": BbrCurrensySpider,
    "VkClipsSpider": VkClipsSpider
}


class Command(BaseCommand):
    help = 'Запуск Scrapy-пауков'

    def add_arguments(self, parser):
        # Добавляем аргумент для выбора паука
        parser.add_argument(
            'spider_name',
            type=str,
            help='Имя паука для запуска (например, "my_spider" или "another_spider")',
        )

    def handle(self, *args, **options):
        spider_name = options['spider_name']

        # Проверяем, существует ли паук с таким именем
        if spider_name not in SPIDERS:
            raise CommandError(f'Паук "{spider_name}" не найден. Доступные пауки: {", ".join(SPIDERS.keys())}')

        # Запускаем выбранного паука
        process = CrawlerProcess(get_project_settings())
        process.crawl(SPIDERS[spider_name])
        process.start()

        self.stdout.write(self.style.SUCCESS(f'Паук "{spider_name}" успешно завершил работу'))
