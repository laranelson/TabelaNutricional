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
    vitamina_d = models.FloatField('Vitamina D (µg)', default=0.0)
    vitamina_c = models.FloatField('Vitamina C (mg)', default=0.0)
    vitamina_e = models.FloatField('Vitamina E (mg)', default=0.0)
    tiamina = models.FloatField('Tiamina (mg)', default=0.0)
    riboflavina = models.FloatField('Riboflavina (mg)', default=0.0)
    niacina = models.FloatField('Niacina (mg)', default=0.0)
    vitamina_b6 = models.FloatField('Vitamina B6 (mg)', default=0.0)
    vitamina_b9 = models.FloatField('Vitamina B9 (mg)', default=0.0)
    acido_folico = models.FloatField('Ácido Fólico (µg)', default=0.0)
    vitamina_b12 = models.FloatField('Vitamina B12 (µg)', default=0.0)
    biotina = models.FloatField('Biotina (µg)', default=0.0)
    acido_pantotenico = models.FloatField('Ácido Pantotênico (µg)', default=0.0)
    calcio = models.FloatField('Cálcio (mg)', default=0.0)
    ferro = models.FloatField('Ferro(mg)', default=0.0)
    magnesio = models.FloatField('Magnésio (mg)', default=0.0)
    zinco = models.FloatField('Zinco (mg)', default=0.0)
    iodo = models.FloatField('Iodo (µg)', default=0.0)
    vitamina_k = models.FloatField('Vitamina K (µg)', default=0.0)
    fosforo = models.FloatField('Fósforo (mg)', default=0.0)
    fluor = models.FloatField('Flúor (mg)', default=0.0)
    cobre = models.FloatField('Cobre (mg)', default=0.0)
    selenio = models.FloatField('Selênio (µg)', default=0.0)
    molibdenio = models.FloatField('Molibdênio (µg)', default=0.0)
    cromo = models.FloatField('Cromo (µg)', default=0.0)
    manganes = models.FloatField('Manganês (mg)', default=0.0)
    colina = models.FloatField('Colina (mg)', default=0.0)
    potassio = models.FloatField('Potássio (mg)', default=0.0)
    gorduras_monoinsaturadas = models.FloatField('Gorduras monoinsaturadas (g)', default=0.0)
    colesterol = models.FloatField('Colesterol (mg)', default=0.0)
    gorduras_omega3 = models.FloatField('Gorduras poli-insaturadas, Ômega 3 (g)', default=0.0)
    gorduras_omega6 = models.FloatField('Gorduras poli-insaturadas, Ômega 6 (g)', default=0.0)
    acido_omega3 = models.FloatField('Ácido alfa-linolênico Ômega 3 (mg)', default=0.0)
    acido_omega6 = models.FloatField('Ácido alfa-linolênico Ômega 6 (mg)', default=0.0)

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







