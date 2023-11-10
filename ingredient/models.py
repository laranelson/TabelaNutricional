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
    carboidrato = models.FloatField('Carboidrato (g)', default=0.0)
    acucares_totais = models.FloatField('Açúcares totais (g)', default=0.0)
    acucares_adicionados = models.FloatField('Açúcares adicionados (g)', default=0.0)
    proteina = models.FloatField('Proteína (g)', default=0.0)
    gorduras_totais = models.FloatField('Gorduras Totais (g)', default=0.0)
    gorduras_saturadas = models.FloatField('Gorduras Saturadas (g)', default=0.0)
    gorduras_trans = models.FloatField('Gorduras Trans (g)', default=0.0)
    fibra_alimentar = models.FloatField('Fibra Alimentar (g)', default=0.0)
    sodio = models.FloatField('Sódio (mg)', default=0.0)
    vitamina_a = models.FloatField('Vitamina A (µg)', default=0.0)


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







