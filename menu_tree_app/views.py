from typing import List, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import MenuItem


def build_menu_tree(
		items: List[MenuItem],
		parent_id: int = None,
		current_url:  str = None,
		active_items: set = set()) -> List[Dict]:
	"""
	Метод, который рекурсивно строит древовидную структуру меню.
	"""
	tree = []
	for item in items:
		if item.parent_id == parent_id:
			node = {
				'item': item,
				'is_current': item.url == current_url,
				'is_active': item.id in active_items or item.url == current_url,
				'children': [],
			}

			node['children'] = build_menu_tree(
				items,
				parent_id=item.id,
				current_url=current_url,
				active_items=active_items
			)
			tree.append(node)

	return tree


def menu_view(request: HttpRequest) -> HttpResponse:
	current_url = request.path

	# Получаем все пункты меню и предварительно загружаем дочерние элементы для оптимизации
	menu_items = MenuItem.objects.prefetch_related('children').order_by('position')

	# Список для активных и видимых пунктов меню
	active_item_ids = set()
	for item in menu_items:
		if item.is_currently_active(current_url=current_url):
			active_item_ids.add(item.id)
			active_item_ids.update([ancestor.id for ancestor in item.get_ancestors()])

	menu_tree = build_menu_tree(list(menu_items), current_url=current_url, active_items=active_item_ids)

	context = {
		'main_menu': menu_tree,
	}

	return render(request, 'menu_tree_app/menu.html', context=context)
