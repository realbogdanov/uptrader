from typing import List, Dict

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def draw_menu(menu_tree: List) -> str:
	"""
	Отрисовывает меню на основе предоставленной структуры дерева.

	Args:
	    menu_tree (List): Структура дерева меню.

	Returns:
	    str: HTML код меню.
	"""
	def render_menu_item(node: Dict) -> str:
		item = node['item']

		# Определяем, является ли пункт активным
		active_class = 'active' if node['is_active'] else ''

		# Формируем HTML для дочерних пунктов меню, если они есть.
		children_html = ''.join([render_menu_item(child) for child in node['children']])
		children_html_safe = mark_safe(children_html)

		if children_html:
			return format_html(
				'<li class="{}"><a href="{}">{}</a><ul>{}</ul></li>',
				active_class,
				item.url,
				item.name,
				children_html_safe
			)
		else:
			return format_html(
				'<li class="{}"><a href="{}">{}</a></li>',
				active_class,
				item.url,
				item.name
			)

	menu_html = ''.join([render_menu_item(node) for node in menu_tree])

	# Возвращаем HTML как безопасный (safe) текст
	return format_html('<ul>{}</ul>', mark_safe(menu_html))
