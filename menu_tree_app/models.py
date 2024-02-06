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
	- parent: Ссылка на родительский пункт меню (ForeignKey на себя же). Если None, пункт считается корневым.
	"""

	name = models.CharField(max_length=100)
	url = models.CharField(max_length=4096)
	position = models.PositiveIntegerField()
	is_active = models.BooleanField(default=True)
	icon = models.CharField(max_length=100, blank=True)
	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='children'
	)

	def __str__(self):
		return self.name
