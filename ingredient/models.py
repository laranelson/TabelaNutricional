#from wsgiref.util import request_uri
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator



class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField('Ingrediente', max_length=30)
    portion = models.FloatField('Porção (g)', validators=[MinValueValidator(0.1)])
    carboidrato = models.FloatField('Carboidrato (g)')
    acucares_totais = models.FloatField('Açúcares totais (g)')
    acucares_adicionados = models.FloatField('Açúcares adicionados (g)')
    proteina = models.FloatField('Proteína (g)')
    gorduras_totais = models.FloatField('Gorduras Totais (g)')
    gorduras_saturadas = models.FloatField('Gorduras Saturadas (g)')
    gorduras_trans = models.FloatField('Gorduras Trans (g)')
    fibra_alimentar = models.FloatField('Fibra Alimentar (g)')
    sodio = models.FloatField('Sódio (mg)')

    def __str__(self):
        return self.name
        
    def clean(self):
        if self.portion <= 0:
            raise ValidationError('O valor da porção deve ser maior que zero.')

    def get_absolute_url(self):
        return reverse("ingredient:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("ingredient:delete", kwargs={"id": self.id})

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        db_table = "ingredient"







