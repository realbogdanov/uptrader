# Generated by Django 5.0.1 on 2024-02-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_tree_app', '0002_menuitem_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='menu_name',
            field=models.CharField(default='main_menu', help_text='Название меню, к которому принадлежит пункт', max_length=100),
        ),
    ]
