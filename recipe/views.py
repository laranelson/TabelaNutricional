
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from recipe.forms import RecipeItemFormSet, RecipeForm
from recipe.models import Recipe
from ingredient.models import Ingredient
from django.urls import reverse
from django.views.generic import (
                                    ListView, 
                                    CreateView, 
                                    UpdateView, 
                                    DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import request

class RecipeListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = 'recipe_list.html'
    paginate_by = 5
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


@login_required  # Certifica-se de que o usuário está logado
def my_view(request):
    user = request.user  # Obtém o usuário logado

    # Filtra os ingredientes com base no usuário logado
    ingredients = Ingredient.objects.filter(user=user)

    return ingredients  # Retorna as opções de ingredientes filtradas para uso posterior


class RecipeCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_create.html'
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        items_formset = RecipeItemFormSet(request.POST)
        if form.is_valid() and items_formset.is_valid():
            return self.form_valid(form, items_formset)
        else:
            return self.form_invalid(form, items_formset)

    def form_valid(self, form, items_formset):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        
        # Associe o objeto RecipeItem à instância Recipe antes de salvar.
        for item in items_formset:
            item_instance = item.save(commit=False)
            item_instance.recipe = self.object
            item_instance.save()

        return redirect(reverse("recipe:list"))

    def get_context_data(self, **kwargs):
        data = super(RecipeCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = RecipeItemFormSet(self.request.POST)
        else:
            data['items_formset'] = RecipeItemFormSet()
            # Obtenha as opções de ingredientes filtradas do método my_view
            ingredients = my_view(self.request)
            # Atribua as opções de ingredientes filtradas a cada formulário no formset
            for form in data['items_formset'].forms:
                form.fields['ingredient'].queryset = ingredients
                
        return data

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('recipe:list')
    template_name = 'recipe_update.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['items_formset'] = RecipeItemFormSet(self.request.POST, instance=self.object, prefix='items')
        else:
            data['items_formset'] = RecipeItemFormSet(instance=self.object, prefix='items')

            # Obtenha as opções de ingredientes filtradas do método my_view
            ingredients = my_view(self.request)
            # Atribua as opções de ingredientes filtradas a cada formulário no formset
            for form in data['items_formset'].forms:
                form.fields['ingredient'].queryset = ingredients

        return data

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            items = context['items_formset']

            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.user = self.request.user  # Atribui o usuário logado ao campo 'user'
                self.object.save()

                if items.is_valid():
                    items.instance = self.object
                    items.save()
                else:
                    return self.render_to_response(self.get_context_data(form=form, items_formset=items))

            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Recipe
    template_name = 'recipe_delete.html'
    success_url = reverse_lazy('recipe:list')



def recipe_list(request):
    search_query = request.GET.get('recipe_search')
    
    if search_query:
        recipe_list = Recipe.objects.filter(user=request.user, name__icontains=search_query)
    else:
        recipe_list = Recipe.objects.filter(user=request.user)

    if not recipe_list:  # Verifica se a lista de ingredientes está vazia
        message = "Desculpe, não foram encontrados receitas com o nome pesquisado."
        return render(request, 'recipe_list.html', {'message': message})
    else:
        return render(request, 'recipe_list.html', {'recipe_list': recipe_list})


