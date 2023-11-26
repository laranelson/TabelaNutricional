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
            'vitamina_a': 0,
            'vitamina_d': 0,
            'vitamina_c': 0,
            'vitamina_e': 0,
            'tiamina': 0,
            'riboflavina': 0,
            'niacina': 0,
            'vitamina_b6': 0,
            'vitamina_b9': 0,
            'acido_folico': 0,
            'vitamina_b12': 0,
            'biotina': 0,
            'acido_pantotenico': 0,
            'calcio': 0,
            'ferro': 0,
            'magnesio': 0,
            'zinco': 0,
            'iodo': 0,
            'vitamina_k': 0,
            'fosforo': 0,
            'fluor': 0,
            'cobre': 0,
            'selenio': 0,
            'molibdenio': 0,
            'cromo': 0,
            'manganes': 0,
            'colina': 0,
            'potassio': 0,
            'gorduras_monoinsaturadas': 0,
            'colesterol': 0,
            'gorduras_omega3': 0,
            'gorduras_omega6': 0,
            'acido_omega3': 0,
            'acido_omega6': 0,
            
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
                'vitamina_a': item.ingredient.vitamina_a / item.ingredient.portion,
                'vitamina_d': item.ingredient.vitamina_d / item.ingredient.portion,
                'vitamina_c': item.ingredient.vitamina_c / item.ingredient.portion,
                'vitamina_e': item.ingredient.vitamina_e / item.ingredient.portion,
                'tiamina': item.ingredient.tiamina / item.ingredient.portion,
                'riboflavina': item.ingredient.riboflavina / item.ingredient.portion,
                'niacina': item.ingredient.niacina / item.ingredient.portion,
                'vitamina_b6': item.ingredient.vitamina_b6 / item.ingredient.portion,
                'vitamina_b9': item.ingredient.vitamina_b9 / item.ingredient.portion,
                'acido_folico': item.ingredient.acido_folico / item.ingredient.portion,
                'vitamina_b12': item.ingredient.vitamina_b12 / item.ingredient.portion,
                'biotina': item.ingredient.biotina / item.ingredient.portion,
                'acido_pantotenico': item.ingredient.acido_pantotenico / item.ingredient.portion,
                'calcio': item.ingredient.calcio / item.ingredient.portion,
                'ferro': item.ingredient.ferro / item.ingredient.portion,
                'magnesio': item.ingredient.magnesio / item.ingredient.portion,
                'zinco': item.ingredient.zinco / item.ingredient.portion,
                'iodo': item.ingredient.iodo / item.ingredient.portion,
                'vitamina_k': item.ingredient.vitamina_k / item.ingredient.portion,
                'fosforo': item.ingredient.fosforo / item.ingredient.portion,
                'fluor': item.ingredient.fluor / item.ingredient.portion,
                'cobre': item.ingredient.cobre / item.ingredient.portion,
                'selenio': item.ingredient.selenio / item.ingredient.portion,
                'molibdenio': item.ingredient.molibdenio / item.ingredient.portion,
                'cromo': item.ingredient.cromo / item.ingredient.portion,
                'manganes': item.ingredient.manganes / item.ingredient.portion,
                'colina': item.ingredient.colina / item.ingredient.portion,
                'potassio': item.ingredient.potassio / item.ingredient.portion,
                'gorduras_monoinsaturadas': item.ingredient.gorduras_monoinsaturadas / item.ingredient.portion,
                'colesterol': item.ingredient.colesterol / item.ingredient.portion,
                'gorduras_omega3': item.ingredient.gorduras_omega3 / item.ingredient.portion,
                'gorduras_omega6': item.ingredient.gorduras_omega6 / item.ingredient.portion,
                'acido_omega3': item.ingredient.acido_omega3 / item.ingredient.portion,
                'acido_omega6': item.ingredient.acido_omega6 / item.ingredient.portion,
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
            'vitamina_a': 'vitamina_a100',
            'vitamina_c': 'vitamina_c100',
            'vitamina_d': 'vitamina_d100', 
            'vitamina_e': 'vitamina_e100',
            'tiamina': 'tiamina100',
            'riboflavina': 'riboflavina100',
            'niacina': 'niacina100',
            'vitamina_b6': 'vitamina_b6100',
            'vitamina_b9': 'vitamina_b9100',
            'acido_folico': 'acido_folico100',
            'vitamina_b12': 'vitamina_b12100',
            'biotina': 'biotina100',
            'acido_pantotenico': 'acido_pantotenico100',
            'calcio': 'calcio100',
            'ferro': 'ferro100',
            'magnesio': 'magnesio100',
            'zinco': 'zinco100',
            'iodo': 'iodo100',
            'vitamina_k': 'vitamina_k100',
            'fosforo': 'fosforo100',
            'fluor': 'fluor100',
            'cobre': 'cobre100',
            'selenio': 'selenio100',
            'molibdenio': 'molibdenio100',
            'cromo': 'cromo100',
            'manganes': 'manganes100',
            'colina': 'colina100',
            'potassio': 'potassio100',
            'gorduras_monoinsaturadas': 'gorduras_monoinsaturadas100',
            'colesterol': 'colesterol100',
            'gorduras_omega3': 'gorduras_omega3100',
            'gorduras_omega6': 'gorduras_omega6100',
            'acido_omega3': 'acido_omega3100',
            'acido_omega6': 'acido_omega6100'
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
        somas['vitamina_a_vd'] = (somas['vitamina_a'] / 800 ) * 100
        somas['vitamina_d_vd'] = (somas['vitamina_d'] / 15 ) * 100
        somas['vitamina_c_vd'] = (somas['vitamina_c'] / 100 ) * 100
        somas['vitamina_e_vd'] = (somas['vitamina_e'] / 15 ) * 100
        somas['tiamina_vd'] = (somas['tiamina'] / 1.2 ) * 100
        somas['riboflavina_vd'] = (somas['riboflavina'] / 1.2 ) * 100
        somas['niacina_vd'] = (somas['niacina'] / 15 ) * 100
        somas['vitamina_b6_vd'] = (somas['vitamina_b6'] / 1.3 ) * 100
        somas['vitamina_b9_vd'] = (somas['vitamina_b9'] / 240 ) * 100
        somas['acido_folico_vd'] = (somas['acido_folico'] / 400 ) * 100
        somas['vitamina_b12_vd'] = (somas['vitamina_b12'] / 2.4 ) * 100
        somas['biotina_vd'] = (somas['biotina'] / 30 ) * 100
        somas['acido_pantotenico_vd'] = (somas['acido_pantotenico'] / 5 ) * 100
        somas['calcio_vd'] = (somas['calcio'] / 1000 ) * 100
        somas['ferro_vd'] = (somas['ferro'] / 14 ) * 100
        somas['magnesio_vd'] = (somas['magnesio'] / 420 ) * 100
        somas['zinco_vd'] = (somas['zinco'] / 11 ) * 100
        somas['iodo_vd'] = (somas['iodo'] / 150 ) * 100
        somas['vitamina_k_vd'] = (somas['vitamina_k'] / 120 ) * 100
        somas['fosforo_vd'] = (somas['fosforo'] / 700 ) * 100
        somas['fluor_vd'] = (somas['fluor'] / 4 ) * 100
        somas['cobre_vd'] = (somas['cobre'] / 900 ) * 100
        somas['selenio_vd'] = (somas['selenio'] / 34 ) * 100
        somas['molibdenio_vd'] = (somas['molibdenio'] / 45 ) * 100
        somas['cromo_vd'] = (somas['cromo'] / 35 ) * 100
        somas['manganes_vd'] = (somas['manganes'] / 3 ) * 100
        somas['colina_vd'] = (somas['colina'] / 550 ) * 100
        somas['potassio_vd'] = (somas['potassio'] / 3500 ) * 100
        somas['gorduras_monoinsaturadas_vd'] = (somas['gorduras_monoinsaturadas'] / 20 ) * 100
        somas['colesterol_vd'] = (somas['colesterol'] / 300 ) * 100
        somas['gorduras_omega3_vd'] = (somas['gorduras_omega3'] / 24 ) * 100
        somas['gorduras_omega6_vd'] = (somas['gorduras_omega6'] / 38 ) * 100
        somas['acido_omega3_vd'] = (somas['acido_omega3'] / 250 ) * 100
        somas['acido_omega6_vd'] = (somas['acido_omega6'] / 500 ) * 100
        
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
