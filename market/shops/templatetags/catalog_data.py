from products.models import Category
from django.template import Library

register = Library()


@register.simple_tag
def query_set():
    """Тег для возвращения данных модели Category в шаблон jinja2."""

    return Category.objects.prefetch_related("parent")
