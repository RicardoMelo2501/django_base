# Generated by Django 4.2.2 on 2023-06-16 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_submenu'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submenu',
            options={'verbose_name': 'Sub Menu', 'verbose_name_plural': 'Sub Menus'},
        ),
    ]