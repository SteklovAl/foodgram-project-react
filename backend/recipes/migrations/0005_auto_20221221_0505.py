# Generated by Django 2.2.16 on 2022-12-21 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221215_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='recipeingredientdetails',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name']},
        ),
    ]