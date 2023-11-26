from django.urls import path
from . import views
from recipe.views import (
                            RecipeListView, 
                            RecipeCreateView, 
                            RecipeUpdateView, 
                            RecipeDeleteView
)



app_name = 'recipe'
urlpatterns = [
    path('recipe/list/', RecipeListView.as_view(), name='list'),
    path('recipe/create/', RecipeCreateView.as_view(), name='create'),
    path('recipe/update/<int:pk>/', RecipeUpdateView.as_view(), name='update'),
    path('recipe/delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete'),
    path('ingredient/recipe_search/', views.recipe_list, name='recipe_search')
]
