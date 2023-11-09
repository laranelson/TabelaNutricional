from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('', include('recipe.urls')),
    path('', include('ingredient.urls')),
    path('', include('core.urls')),
    path('', include('table.urls')),
]
