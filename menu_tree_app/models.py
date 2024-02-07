from typing import List

from django.db import models


class MenuItem(models.Model):
	"""
	Представление пункта меню в базе данных.

	Каждый пункт меню может иметь ссылку на родительский пункт, образуя иерархическую структуру.

	Поля:
	- name: Название пункта меню.
	- url: URL пункта меню, может быть как прямым URL, так и именованным путём Django.
	- position: Позиция пункта меню среди пунктов одного уровня для упорядочивания.
	- is_active: Статус активности пункта меню, используется для управления его отображением.
	- icon: Имя класса иконки для пункта меню (необязательное).
	- menu_name: Название меню, к которому принадлежит пункт.
	- parent: Ссылка на родительский пункт меню (ForeignKey на себя же). Если None, пункт считается корневым.
	"""

	name = models.CharField(max_length=100)
	url = models.CharField(max_length=4096)
	position = models.PositiveIntegerField()
	is_active = models.BooleanField(default=True)
	icon = models.CharField(max_length=100, blank=True)
	menu_name = models.CharField(
		max_length=100,
		default='main_menu',
		help_text='Название меню, к которому принадлежит пункт')
	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='children'
	)

	def __str__(self) -> str:
		return self.name

	def is_currently_active(self, current_url: str) -> bool:
		"""
		Метод, который определяет, является ли данный пункт меню активным на основе текущего URL.

		Пункт считается активным, если его URL совпадает с текущим URL или если любой из его дочерних пунктов активен.
		"""

		# Проверяем URL пункта меню с текущим URL
		if self.url == current_url:
			return True

		# Если нет, проверяем дочерние пункты
		for child in self.children.all():
			if child.is_currently_active(current_url):
				return True

		# В противном случае возвращаем ложное значение
		return False

	def get_ancestors(self) -> List['MenuItem']:
		"""
		Метод, который возвращает всех предков текущего пункта меню.
		"""

		ancestors = []
		parent = self.parent
		while parent is not None:
			ancestors.append(parent)
			parent = parent.parent

		return ancestors

	def get_descendants(self, include_self: bool = False, depth: int = 1) -> List['MenuItem']:
		"""
		Метод, который возвращает всех потомков текущего пункта меню до заданной глубины.
		"""

		descendants = []
		if include_self:
			descendants.append(self)

		for child in self.children.all():
			descendants.append(child)
			if depth > 1:
				descendants.extend(child.get_descendants(depth=depth-1))

		return descendants
