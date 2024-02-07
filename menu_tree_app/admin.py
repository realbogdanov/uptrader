from django.contrib import admin

from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
	"""
	Класс представляющий административный интерфейс для управления элементами меню.

	Attributes:
	    list_display (list): Определяет поля, отображаемые в списке элементов в административной панели.
	    list_filter (list): Определяет поля, по которым можно фильтровать элементы в административной панели.
	    search_fields (list): Определяет поля, по которым можно выполнять поиск элементов в административной панели.
	    fields (list): Определяет поля, отображаемые на странице редактирования элемента меню.
	    raw_id_fields (list): Поле для упрощения выбора родительского элемента.

	"""

	list_display = ['name', 'url', 'position', 'is_active', 'parent', 'menu_name',]
	list_filter = ['is_active', 'parent',]
	search_fields = ['name', 'url',]

	def parent_name(self, obj: MenuItem) -> str:
		"""
		Возвращает имя родительского элемента, если он существует.

		Args:
		    obj (MenuItem): Элемент меню.

		Returns:
		    str: Имя родительского элемента.
		"""
		return obj.parent.name if obj.parent else None
	parent_name.short_description = 'Parent'

	# Настройка формы редактирования
	fields = ['name', 'url', 'position', 'is_active', 'icon', 'parent', 'menu_name',]
	raw_id_fields = ['parent',]


admin.site.register(MenuItem, MenuItemAdmin)
