# Generated by Django 4.2.6 on 2023-10-21 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_recipeitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeitem',
            name='user',
        ),
    ]