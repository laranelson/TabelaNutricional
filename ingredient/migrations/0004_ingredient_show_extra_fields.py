# Generated by Django 4.2.6 on 2023-11-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0003_alter_ingredient_acucares_adicionados_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='show_extra_fields',
            field=models.BooleanField(default=False, verbose_name='Exibir campos adicionais'),
        ),
    ]
