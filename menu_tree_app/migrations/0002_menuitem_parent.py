# Generated by Django 5.0.1 on 2024-02-06 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_tree_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu_tree_app.menuitem'),
        ),
    ]
