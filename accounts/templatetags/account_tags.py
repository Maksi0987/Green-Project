from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def days_on_site(date_joined):
    """Вираховує кількість днів на сайті та правильно відмінює слово 'день'"""
    if not date_joined:
        return ""

    delta = timezone.now() - date_joined
    days_count = delta.days

    if days_count <= 0:
        return "перший день"

    # Правила українського відмінювання
    remainder_100 = days_count % 100
    remainder_10 = days_count % 10

    if 11 <= remainder_100 <= 14:
        word = "днів"
    elif remainder_10 == 1:
        word = "день"
    elif 2 <= remainder_10 <= 4:
        word = "дні"
    else:
        word = "днів"

    return f"{days_count} {word}"