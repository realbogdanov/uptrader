from django import template
from django.utils.html import mark_safe
from ..models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name: str):
	"""
	Template tag для отрисовки древовидного меню.

	Args:
	    menu_name (str): Название меню, которое нужно отрисовать.

	Returns:
	    str: HTML-код для отображения меню.

	Example:
	    {% draw_menu 'main_menu' %}

	Note:
	    Этот template tag извлекает структуру меню из базы данных и формирует HTML-код для отображения меню с заданным
	    названием. Внутри меню каждый пункт представлен в виде ссылки на соответствующий URL. Результат считается безопасным
	    (safe) HTML-текстом и может быть использован в шаблонах.
	"""

	# Извлекаем структуру меню из БД по имени меню
	menu_items = MenuItem.objects.filter(menu_name=menu_name).order_by('position')

	# Формируем HTML для меню
	menu_html = '<ul>'
	for item in menu_items:
		menu_html += f'<li> <a href="{item.url}">{item.name}</a></li>'
	menu_html += '</ul>'

	# Возвращаем HTML как безопасный (safe) текст
	return mark_safe(menu_html)
