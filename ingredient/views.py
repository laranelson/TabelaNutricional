from django.shortcuts import get_object_or_404 
from django.views.generic import (
                                    ListView, 
                                    CreateView, 
                                    UpdateView, 
                                    DeleteView
)
from .models import Ingredient
from .forms import IngredientForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class IngredientListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "ingredient_list.html"
    paginate_by = 5
    model = Ingredient 
    
    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)

class IngredientCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "ingredient_create.html"
    form_class = IngredientForm

    def form_valid(self, form):
        # Atribuir o usuário logado ao campo 'user' antes de salvar o formulário
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ingredient:list")
    
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "ingredient_update.html"
    form_class = IngredientForm
    
    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Ingredient, id=id)

    # validar o formulário | validation the form
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ingredient:list")

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "ingredient_delete.html"
    
    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Ingredient, id=id)

    def get_success_url(self):
        return reverse("ingredient:list")


   
