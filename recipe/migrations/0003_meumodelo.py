# Generated by Django 2.2.13 on 2023-10-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20220807_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeuModelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo', models.FloatField()),
            ],
        ),
    ]