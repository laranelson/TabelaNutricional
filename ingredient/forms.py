from django import forms
from django.forms import fields
from .models import Ingredient


class IngredientForm(forms.ModelForm):

        class Meta:
            model = Ingredient
            exclude = ['user']  # Exclui o campo user do formulário
            

