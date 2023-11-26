from django import forms
from .models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

# Este é um widget personalizado que herda de forms.NumberInput
# Ele é responsável por renderizar o campo de input para floats
# Se o valor for 0.0 ou None, ele renderiza como uma string vazia para ocultar esse valor no formulário
class HiddenDefaultFloatInput(forms.NumberInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value == 0.0 or value is None:
            value = ''  # Se o valor for 0.0 ou None, renderiza como uma string vazia
        return super().render(name, value, attrs, renderer)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        exclude = ['user']  # Exclui o campo 'user' do formulário

    # Este método é executado durante a validação do formulário
    # Ele verifica os campos especificados e se eles estão vazios (None)
    # Se algum campo estiver vazio, ele define o valor para 0.0
    def clean(self):
        cleaned_data = super().clean()  # Obtém os dados limpos do formulário

        # Lista de campos que devem ter valores padrão se estiverem vazios
        fields_to_check = [
            'carboidrato',
            'acucares_totais',
            'acucares_adicionados',
            'proteina',
            'gorduras_totais',
            'gorduras_saturadas',
            'gorduras_trans',
            'fibra_alimentar', 
            'sodio', 
            'vitamina_a',
            'vitamina_d',
            'vitamina_c',
            'vitamina_e',
            'tiamina',
            'riboflavina',
            'niacina',
            'vitamina_b6',
            'vitamina_b9',
            'acido_folico',
            'vitamina_b12',
            'biotina',
            'acido_pantotenico',
            'calcio',
            'ferro',
            'magnesio',
            'zinco',
            'iodo',
            'vitamina_k',
            'fosforo',
            'fluor',
            'cobre',
            'selenio',
            'molibdenio',
            'cromo',
            'manganes',
            'colina',
            'potassio',
            'gorduras_monoinsaturadas',
            'colesterol',
            'gorduras_omega3',
            'gorduras_omega6',
            'acido_omega3',
            'acido_omega6'
        ]

        # Verifica se os campos estão vazios e, se estiverem, define o valor para 0.0
        for field in fields_to_check:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0.0  # Se nenhum valor for fornecido, use o valor padrão 0.0

        return cleaned_data  # Retorna os dados limpos após as alterações, se necessário

    # Este método é chamado na inicialização do formulário
    # Ele configura os widgets dos campos para usar o HiddenDefaultFloatInput (ocultar 0.0)
    # Além disso, define os campos como não obrigatórios e com valor inicial None para evitar a exibição de 0.0 no formulário
    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('portion'),
                Field('carboidrato'),
                Field('acucares_totais'),
                Field('acucares_adicionados'),
                Field('proteina'),
                Field('gorduras_totais'),
                Field('gorduras_saturadas'),
                Field('gorduras_trans'),
                Field('fibra_alimentar'),
                Field('sodio'),
            ),
            
            Div(
                Field('vitamina_a'),
                Field('vitamina_d'),
                Field('vitamina_c'),
                Field('vitamina_e'),
                Field('tiamina'),
                Field('riboflavina'),
                Field('niacina'),
                Field('vitamina_b6'),
                Field('vitamina_b9'),
                Field('acido_folico'),
                Field('vitamina_b12'),
                Field('biotina'),
                Field('acido_pantotenico'),
                Field('calcio'),
                Field('ferro'),
                Field('magnesio'),
                Field('zinco'),
                Field('iodo'),
                Field('vitamina_k'),
                Field('fosforo'),
                Field('fluor'),
                Field('cobre'),
                Field('selenio'),
                Field('molibdenio'),
                Field('cromo'),
                Field('manganes'),
                Field('colina'),
                Field('potassio'),
                Field('gorduras_monoinsaturadas'),
                Field('colesterol'),
                Field('gorduras_omega3'),
                Field('gorduras_omega6'),
                Field('acido_omega3'),
                Field('acido_omega6'),
                css_class='ocultar'
            )
        )

        # Lista de campos para os quais queremos ocultar o valor 0.0
        fields_to_hide = [
            'carboidrato',
            'acucares_totais',
            'acucares_adicionados',
            'proteina',
            'gorduras_totais',
            'gorduras_saturadas',
            'gorduras_trans',
            'fibra_alimentar', 
            'sodio', 
            'vitamina_a',
            'vitamina_d',
            'vitamina_c',
            'vitamina_e',
            'tiamina',
            'riboflavina',
            'niacina',
            'vitamina_b6',
            'vitamina_b9',
            'acido_folico',
            'vitamina_b12',
            'biotina',
            'acido_pantotenico',
            'calcio',
            'ferro',
            'magnesio',
            'zinco',
            'iodo',
            'vitamina_k',
            'fosforo',
            'fluor',
            'cobre',
            'selenio',
            'molibdenio',
            'cromo',
            'manganes',
            'colina',
            'potassio',
            'gorduras_monoinsaturadas',
            'colesterol',
            'gorduras_omega3',
            'gorduras_omega6',
            'acido_omega3',
            'acido_omega6'
        ]

        # Para cada campo, configura o widget para ocultar o 0.0, define como não obrigatório e inicializa como None
        for field_name in fields_to_hide:
            self.fields[field_name].widget = HiddenDefaultFloatInput()
            self.fields[field_name].required = False
            self.fields[field_name].initial = None  # Define o valor inicial como None para evitar a exibição do 0.0
