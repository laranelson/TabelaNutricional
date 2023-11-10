from recipe.models import Recipe, RecipeItem
from django.db.models import Sum
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

#import para gerar o relatorio PDF do def render_pdf_view(request):
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#import para visualizar PDF def def pdf_view(_request, file_name):
import os
from django.conf import settings



class NutritionTableListView(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Recipe
    template_name = 'table_create.html'
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

        # Calcula o valor proporcional de cada RecipeItem e as somas
        recipe_items = RecipeItem.objects.filter(recipe=recipe)
        somas = {
            'carboidrato': 0,
            'acucares_totais': 0,
            'acucares_adicionados': 0,
            'proteina': 0,
            'gorduras_totais': 0,
            'gorduras_saturadas': 0,
            'gorduras_trans': 0,
            'fibra_alimentar': 0,
            'sodio': 0,
        }

        for item in recipe_items:
            item.proportional_value = item.value / (total_value / recipe.portion)

            # Calcula os valores proporcionalmente com base no Ingredient
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

            for key, ratio in ratios.items():
                if item.ingredient.portion:
                    value = ratio * item.proportional_value
                    setattr(item, key, value)
                    somas[key] += value
                    
        # Calcula o valor kcal diretamente no dicionário somas
        somas['kcal'] = (somas['carboidrato'] * 4) + (somas['proteina'] * 4) + (somas['gorduras_totais'] * 9)
        
        # CALCULOS PARA O VALOR PADRÃO DE 100g
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
                
        somas['kcal_vd'] = (somas['kcal'] / 2000) * 100
        somas['carboidrato_vd'] = (somas['carboidrato'] / 300) * 100
        somas['acucares_totais_vd'] = (somas['acucares_totais'] / 25 ) * 100
        somas['acucares_adicionados_vd'] = (somas['acucares_adicionados'] / 50 ) * 100
        somas['proteina_vd'] = (somas['proteina'] / 50 ) * 100
        somas['gorduras_totais_vd'] = (somas['gorduras_totais'] / 65 ) * 100
        somas['gorduras_saturadas_vd'] = (somas['gorduras_saturadas'] / 20 ) * 100
        somas['gorduras_trans_vd'] = (somas['gorduras_trans'] / 2 ) * 100
        somas['fibra_alimentar_vd'] = (somas['fibra_alimentar'] / 25 ) * 100
        somas['sodio_vd'] = (somas['sodio'] / 2000 ) * 100
        
        # Adicionando as somas calculadas ao contexto
        context.update(somas)
        
        #REPASSANDO O NOME DA RECEITA PARA SER UTILIZADA PARA GERAR O PDF COM O NOME DA RECEITA.PDF 
        context['recipe_name'] = recipe.name
       
        return context
    

def generate_pdf_report(request, pk):
    # Use a mesma lógica da sua NutritionTableListView para obter os dados do modelo Recipe
    recipe_view = NutritionTableListView.as_view()
    response = recipe_view(request, pk=pk)
    
    #ATRIBUIR O NOME DA RECEITA
    nome_do_arquivo = response.context_data['recipe_name']
    
    if response.status_code != 200:
        return HttpResponse('Ocorreu um erro ao gerar o PDF.')

    # Acesse o contexto usando .context_data
    context = response.context_data



    # Renderize o template em HTML para o PDF
    template_path = 'table_pdf.html'  # Substitua pelo caminho para seu novo template HTML
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="Tabela Nutricional ({nome_do_arquivo}).pdf"'
    

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocorreu um erro ao gerar o PDF.')

    return response



def pdf_view(_request, file_name):
    pdf_path = os.path.join(settings.STATIC_ROOT, 'pdf', file_name)
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={file_name}'
            return response
    except FileNotFoundError:
        return HttpResponse('Arquivo não encontrado', status=404)
    except Exception as e:
        return HttpResponse(f'Erro ao processar o arquivo: {e}', status=500)
