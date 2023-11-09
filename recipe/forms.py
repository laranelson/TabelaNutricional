#from crispy_forms.layout import Submit, Layout, Div, Field, Fieldset, HTML, ButtonHolder ----SERVE PRA ALGO???
from django import forms
from django.forms import models, inlineformset_factory
#from crispy_forms.helper import FormHelper ----SERVE PRA ALGO???

#from recipe.custom_layout_object import Formset ----SERVE PRA ALGO???
from recipe.models import Recipe, RecipeItem


class RecipeForm(models.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['user']  # Exclui o campo user do formulário


class RecipeItemForm(forms.ModelForm):
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