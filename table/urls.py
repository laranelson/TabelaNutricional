from django.urls import path
from table.views import NutritionTableListView, pdf_view
from . import views


app_name = 'table'
urlpatterns = [
    path('table/<int:pk>', NutritionTableListView.as_view(), name='table'),
    path('gerar_tabela_pdf/<int:pk>/', views.generate_pdf_report, name='gerar_tabela_pdf'),
    path('visualizar-pdf/<path:file_name>/', pdf_view, name='pdf_view'),
]
