# from cProfile import label
from django.db import models
from django.contrib.auth.models import User 
from ingredient.models import Ingredient
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Recipe(models.Model):
    MEASURE_CHOICE = (
        ('unidade', '1 Unidade'),
        ('xicara', '1 Xícara'),
        ('fatia', '1 Fatia'),
        ('prato', '1 Prato'),
        ('bola', '1 Bola'),
        ('colher_sopa', '1 Colher de Sopa'),
        ('colher_cha', '1 Colher de Chá'),
        ('colher_cafe', '1 Colher de Café'),   
    )
    name = models.CharField('Nome da Receita', max_length=100)
    portions = models.FloatField('Porções por embalagem')
    portion = models.FloatField('Valor da porção (g)', validators=[MinValueValidator(0.1)])
    measure = models.CharField('Medida Caseira', max_length=20, choices=MEASURE_CHOICE, default='unidade')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
    
    def clean(self):
        if self.portion <= 0:
            raise ValidationError('O valor da porção deve ser maior que zero.')
      
    def __str__(self):
        return self.name


class RecipeItem(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ingrediente')
    value = models.FloatField('Valor em (g)')
    #user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    class Meta:
        verbose_name = 'item da Receita'
        
        verbose_name_plural = 'Itens da Receita'
          
    def __str__(self):
        return str(self.recipe)



   
