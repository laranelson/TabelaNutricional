
from django.urls import path
from django.views.generic import TemplateView # path('', TemplateView.as_view(template_name="index.html") )
from django.contrib.auth.decorators import login_required
from core import views
from django.contrib.auth import views as auth_views

from .views import IndexView
urlpatterns = [
    path("", (IndexView.as_view(template_name="core/index.html")), name="index"),
    path("app/", login_required(IndexView.as_view(template_name="core/app.html")), name="app"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("login/submit", views.submit_login, name="submit_login"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password/password-reset.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password/password-reset-done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password-reset-confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password/password-reset-complete.html"), name='password_reset_complete'),
    
]




