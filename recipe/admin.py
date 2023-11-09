from django.contrib import admin

from recipe.models import Recipe, RecipeItem


class RecipeItemInline(admin.TabularInline):
    model = RecipeItem


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    inlines = [
        RecipeItemInline
    ]

@admin.register(RecipeItem)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient',)
    
