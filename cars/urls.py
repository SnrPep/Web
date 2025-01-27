from django.urls import path
from . import views
import os
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('catalog/', views.car_catalog, name='car_catalog'),
    path('get-models/', views.get_models_by_brand, name='get_models'),  # Новый маршрут для AJAX-запроса
    path('check-images/', views.check_images, name='check_images'),
    path('catalog/<str:country>/', views.car_catalog, name='car_catalog_by_country'),
    path('<str:country>/', views.car_list, name='car_catalog_by_country'),
]

# if settings.DEBUG:  # Только для разработки
#     # urlpatterns += static('media/', document_root=os.path.join(settings.BASE_DIR, 'media'))
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)