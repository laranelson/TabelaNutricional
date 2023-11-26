from django import forms
from django.forms import models, inlineformset_factory

from recipe.models import Recipe, RecipeItem


class RecipeForm(models.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['user']  # Exclui o campo user do formulário


class RecipeItemForm(forms.ModelForm):
    value = forms.CharField(
        label='Seu Label',
        widget=forms.TextInput(attrs={'size': '22', 'placeholder': 'quantidade em gramas (g)'})
    )
    class Meta:
        model = RecipeItem
        fields = '__all__'

RecipeItemFormSet = inlineformset_factory(
    Recipe, 
    RecipeItem, 
    RecipeItemForm, 
    max_num=50, 
    min_num=1,
    validate_min=True, 
    extra=0
    )