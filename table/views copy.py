from django.shortcuts import render
from django.db.models.query import QuerySet
from recipe.models import Recipe, RecipeItem
from django.views.generic import ListView
from django.db.models import Sum

from django.views.generic.detail import DetailView # 


class NutritionTableListView(DetailView):
    model = Recipe
    template_name = 'table/soma_template.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenha o registro Recipe associado à visualização
        recipe = context['recipe']
        
        # Calcule a soma do campo 'value' do modelo RecipeItem relacionado a este Recipe
        total_value = RecipeItem.objects.filter(recipe=recipe).aggregate(total_value=Sum('value'))['total_value'] or 0.0
        
        # Realize a divisão de total_value por recipe.portion
        if recipe.portion:
            calculated_value = total_value / recipe.portion
        else:
            calculated_value = 0.0
        
        context['total_value'] = total_value  # Valor total da soma
        context['calculated_value'] = calculated_value  # Valor calculado após a divisão
        
        # Calcula o valor proporcional de cada RecipeItem
        recipe_items = RecipeItem.objects.filter(recipe=recipe)
        for item in recipe_items:
            item.proportional_value = item.value / (total_value / recipe.portion)
            
            
            # Crie um dicionário de rácios para os atributos do Ingredient ratios em português é índices
            ratios = {
                'carboidrato': item.ingredient.carboidrato / item.ingredient.portion,
                'acucares_totais': item.ingredient.acucares_totais / item.ingredient.portion,
                'acucares_adicionados': item.ingredient.acucares_adicionados / item.ingredient.portion,
                'proteina': item.ingredient.proteina / item.ingredient.portion,
                'gorduras_totais': item.ingredient.gorduras_totais / item.ingredient.portion,
                'gorduras_saturadas': item.ingredient.gorduras_saturadas / item.ingredient.portion,
                'gorduras_trans': item.ingredient.gorduras_trans / item.ingredient.portion,
                'fibra_alimentar': item.ingredient.fibra_alimentar / item.ingredient.portion,
                'sodio': item.ingredient.sodio / item.ingredient.portion,
            }

            # Use os rácios para calcular os valores proporcionalmente
            for key, ratio in ratios.items():
                if item.ingredient.portion:
                    setattr(item, key, ratio * item.proportional_value)
                else:
                    setattr(item, key, 0.0)
            
            """
            # Calculos 
            if item.ingredient.portion:
                item.carboidrato = (item.ingredient.carboidrato / item.ingredient.portion) * item.proportional_value
                item.acucares_totais = (item.ingredient.acucares_totais / item.ingredient.portion) * item.proportional_value
                item.acucares_adicionados = (item.ingredient.acucares_adicionados / item.ingredient.portion) * item.proportional_value
                item.proteina = (item.ingredient.proteina / item.ingredient.portion) * item.proportional_value
                item.gorduras_totais = (item.ingredient.gorduras_totais / item.ingredient.portion) * item.proportional_value
                item.gorduras_saturadas = (item.ingredient.gorduras_saturadas / item.ingredient.portion) * item.proportional_value
                item.gorduras_trans = (item.ingredient.gorduras_trans / item.ingredient.portion) * item.proportional_value
                item.fibra_alimentar = (item.ingredient.fibra_alimentar / item.ingredient.portion) * item.proportional_value
                item.sodio = (item.ingredient.sodio / item.ingredient.portion) * item.proportional_value
            else:
                item.carboidrato = 0.0
                item.acucares_totais = 0.0
                item.acucares_adicionados = 0.0
                item.proteina = 0.0
                item.gorduras_totais = 0.0
                item.gorduras_saturadas = 0.0
                item.gorduras_trans = 0.0
                item.fibra_alimentar = 0.0
                item.sodio = 0.0
           """
                
        # DEPOIS POSSO APAGAR ESSE CONTEXT ABAIXO. ELE SÓ SERVE PARA EXIBIR OS TODAS AS LINHAS
        context['recipe_items'] = recipe_items  # Adicione os itens de RecipeItem atualizados ao contexto
                
        somas = {
            'carboidrato_total': 0,
            'acucares_totais': 0,
            'acucares_adicionados': 0,
            'proteina': 0,
            'gorduras_totais': 0,
            'gorduras_saturadas': 0,
            'gorduras_trans': 0,
            'fibra_alimentar': 0,
            'sodio': 0,
            # Adicione outros campos conforme necessário
        }

        # Calcula as somas dos valores para todos os RecipeItems
        for item in recipe_items:
            somas['carboidrato_total'] += item.carboidrato
            somas['acucares_totais'] += item.acucares_totais
            somas['acucares_adicionados'] += item.acucares_adicionados
            somas['proteina'] += item.proteina
            somas['gorduras_totais'] += item.gorduras_totais
            somas['gorduras_saturadas'] += item.gorduras_saturadas
            somas['gorduras_trans'] += item.gorduras_trans
            somas['fibra_alimentar'] += item.fibra_alimentar
            somas['sodio'] += item.sodio
            # Adicione outros campos ao dicionário e calcule suas somas

        # Adicione as somas calculadas ao contexto
        context.update(somas)   
        
        
         # Calcula o valor do kcal código de autoria Nelson Lara
        c = somas['carboidrato']
        p = somas['proteina']
        g = somas['gorduras_totais']
        kcal = (c*4)+(p*4)+(g*9)
        # Adicione o valor do kcal ao contexto
        context['kcal'] = kcal  
        # Calcula o valor kcal diretamente no dicionário somas
        somas['kcal'] = (somas['carboidrato'] * 4) + (somas['proteina'] * 4) + (somas['gorduras_totais'] * 9)
        
        # Define os rótulos e campos que deseja calcular
        calculated_fields = {
            'kcal': 'kcal100',
            'carboidrato': 'carboidrato100',
            'acucares_totais': 'acucares_totais100',
            'acucares_adicionados': 'acucares_adicionados100',
            'proteina': 'proteina100' ,
            'gorduras_totais': 'gorduras_totais100',
            'gorduras_saturadas': 'gorduras_saturadas100',
            'gorduras_trans': 'gorduras_trans100',
            'fibra_alimentar': 'fibra_alimentar100' ,
            'sodio': 'sodio100',
            # Adicione outros campos conforme necessário
        }

        # Calcula os campos proporcionais
        for field, calculated_field in calculated_fields.items():
            if recipe.portion:
                somas[calculated_field] = somas[field] / recipe.portion * 100
            else:
                somas[calculated_field] = 0  # Lida com o caso de divisão por zero

        
        #somas['kcal100'] = somas['kcal'] / recipe.portion * 100
        #somas['carboidrato100'] = somas['carboidrato'] / recipe.portion * 100
        #somas['acucares_totais100'] = somas['acucares_totais'] / recipe.portion * 100
        # Adicionando as somas calculadas ao contexto
        context.update(somas)
           
        return context



"""
class NutritionTableListView(DetailView):
    model = Recipe
    template_name = 'table/soma_template.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenha o registro Recipe associado à visualização
        recipe = context['recipe']
        
        # Calcule a soma do campo 'value' do modelo RecipeItem relacionado a este Recipe
        total_value = RecipeItem.objects.filter(recipe=recipe).aggregate(total_value=Sum('value'))['total_value'] or 0.0
        
        # Realize a divisão de total_value por recipe.portion
        if recipe.portion:
            calculated_value = total_value / recipe.portion
        else:
            calculated_value = 0.0
        
        context['total_value'] = total_value  # Valor total da soma
        context['calculated_value'] = calculated_value  # Valor calculado após a divisão
        
        return context"""

def somar_campos(request):
    
         
    # Encontre o registro específico pelo ID
    registro = Recipe.objects.get(id=1)
    item = RecipeItem.objects.get(id=1)
    
    # Calcule a soma dos campos
    soma_total = registro.portion + 10

    # Renderize o template e passe a soma para ele
    return render(request, 'table/soma_template.html', 
                  {'recipe_name': registro.name, 
                   'recipe_portions': registro.portions, 
                   'recipe_portion': registro.portion,
                   'recipeitem_portion': item.ingredient, 
                   'soma_total': soma_total})

