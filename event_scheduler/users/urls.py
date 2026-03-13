# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('change/', views.CustomUserChangeView, name='change'),
    path('signup/', views.RegisterView, name='signup'),
]
