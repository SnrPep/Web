import django_filters
from .models import Cars,Brands

class CarFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(
        queryset=Brands.objects.all().order_by('brand'),
        field_name="brand_country__brand",
        label="",
        empty_label="Марка авто"
    )
    # country = django_filters.ChoiceFilter(
    #     choices=lambda: [(country, country) for country in
    #                      Brands.objects.values_list('country', flat=True).distinct()],
    #     field_name="brand_country__country",
    #     label="Страна производитель"
    # )
    model = django_filters.ChoiceFilter(
        choices=lambda: [(model, model) for model in
                         Cars.objects.values_list('model', flat=True).distinct().order_by('model')],
        label="",
        empty_label="Модель авто"
    )

    year_from = django_filters.ChoiceFilter(
        field_name="year",
        lookup_expr="gte",  # Больше или равно
        choices=lambda: [(year, year) for year in
                         Cars.objects.values_list('year', flat=True).distinct().order_by('year')],
        label="",
        empty_label="Год от"
    )
    year_to = django_filters.ChoiceFilter(
        field_name="year",
        lookup_expr="lte",  # Меньше или равно
        choices=lambda: [(year, year) for year in
                         Cars.objects.values_list('year', flat=True).distinct().order_by('year')],
        label="",
        empty_label="до"
    )

    mileage_from = django_filters.ChoiceFilter(
        field_name="mileage",
        lookup_expr="gte",
        choices=lambda: [(mileage, mileage) for mileage in
                         Cars.objects.values_list('mileage', flat=True).distinct().order_by('mileage')],
        label="",
        empty_label="Пробег от"
    )

    mileage_to = django_filters.ChoiceFilter(
        field_name="mileage",
        lookup_expr="lte",
        choices=lambda: [(mileage, mileage) for mileage in
                         Cars.objects.values_list('mileage', flat=True).distinct().order_by('mileage')],
        label="",
        empty_label="до"
    )
    # mileage = django_filters.RangeFilter(label='Пробег')

    color = django_filters.ChoiceFilter(
        choices=lambda: [(color, color) for color in
                         Cars.objects.values_list('color', flat=True).distinct().order_by('color')],
        label="",
        empty_label="Цвет"
    )

    transmission = django_filters.ChoiceFilter(
        choices=lambda: [(transmission, transmission) for transmission in
                         Cars.objects.values_list('transmission', flat=True).distinct().order_by('transmission')],
        label="",
        empty_label="Тип КПП"
    )

    drive = django_filters.ChoiceFilter(
        choices=lambda: [(drive, drive) for drive in
                         Cars.objects.values_list('drive', flat=True).distinct().order_by('drive')],
        label="",
        empty_label="Привод"
    )

    class Meta:
        model = Cars
        fields = ['brand', 'model', 'year_from','year_to', 'mileage_from', 'mileage_to', 'color', 'transmission', 'drive']