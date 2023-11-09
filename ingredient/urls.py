from django.urls import path
from .views import (
                    IngredientListView, 
                    IngredientCreateView, 
                    IngredientUpdateView, 
                    IngredientDeleteView
)


app_name = "ingredient"

urlpatterns = [
    path("ingredient/list/", IngredientListView.as_view(), name="list"),
    path("ingredient/create/", IngredientCreateView.as_view(), name="create"),
    path("ingredient/update/<int:id>/", IngredientUpdateView.as_view(), name="update"),
    path("ingredient/delete/<int:id>/", IngredientDeleteView.as_view(), name="delete")
]