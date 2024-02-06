from django.urls import path
from .views import menu_view

app_name = 'menu_tree_app'

urlpatterns = [
    path('', menu_view, name='index_menu'),
]
