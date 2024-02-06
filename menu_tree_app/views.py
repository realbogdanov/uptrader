from typing import List, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import MenuItem


def build_menu_tree(menu_items: List[MenuItem]) -> List[MenuItem]:
	"""
	Функция для построения древовидной структуры меню из плоского списка элементов меню.

	Args:
	    menu_items (List[MenuItem]): Список элементов меню из базы данных.

	Returns:
	    List[MenuItem]: Список верхне уровневых элементов меню, образующих структуру дерева.
	"""

	# Создаём словарь для быстрого доступа к элементам по их id
	menu_items_dict: Dict[int, MenuItem] = {}
	for item in menu_items:
		menu_items_dict[item.id] = item

	# Инициализация children как пустого списка для каждого элемента.
	for item in menu_items:
		item.children = []

	# Список для корневых элементов
	root_menu_items = []
	for item in menu_items:
		if item.parent_id is None:
			root_menu_items.append(item)
		else:
			parent_item = menu_items_dict.get(item.parent_id)
			if parent_item:
				parent_item.children.append(item)

	return root_menu_items


def menu_view(request: HttpRequest):
	menu_items = MenuItem.objects.prefetch_related('children').all()
	menu_tree = build_menu_tree(menu_items)

	# Определение активного пункта меню
	current_url = request.path
	for item in menu_items:
		if current_url == item.url:
			item.is_active = True
		else:
			item.is_active = False

	context = {
		'main_menu': menu_tree
	}
	return render(request, 'menu_tree_app/menu.html', context=context)
