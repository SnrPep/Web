import django_filters
from .models import Cars

class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name="brand_country__brand", lookup_expr='icontains', label='Марка')
    country = django_filters.CharFilter(field_name="brand_country__country", lookup_expr='icontains', label='Страна производитель')
    model = django_filters.CharFilter(lookup_expr='icontains', label='Модель')
    year = django_filters.RangeFilter(label='Год выпуска')
    price = django_filters.RangeFilter(label='Цена')
    mileage = django_filters.RangeFilter(label='Пробег')
    color = django_filters.CharFilter(lookup_expr='icontains', label='Цвет')
    transmission = django_filters.ChoiceFilter(choices=[
        ('Механика', 'Механика'),
        ('Автомат', 'Автоматическая'),
    ], label='Коробка передач')
    drive = django_filters.CharFilter(lookup_expr='icontains', label='Привод')

    class Meta:
        model = Cars
        fields = ['brand','country', 'model', 'year', 'price', 'mileage', 'color', 'transmission', 'drive']