from __future__ import absolute_import, unicode_literals

# Импортируем приложение Celery
from TomikoTradeProject.celery import app as celery_app

# Экспортируем Celery как часть пакета
__all__ = ('celery_app',)