from django import template

register = template.Library()

@register.filter
def times(number):
    """Возвращает range для использования в шаблоне"""
    return range(number)
@register.filter
def sub(value, arg):
    """Вычитает arg из value"""
    return value - arg