from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agent1/', views.agent1, name='agent1'),
    path('agent1_handler/', views.agent1_handler, name='agent1_handler'),
    path('agent2/', views.agent2, name='agent2'),
    path('agent2_handler/', views.agent2_handler, name='agent2_handler'),
    path('agent3/', views.agent3, name='agent3'),
    path('agent3_handler/', views.agent3_handler, name='agent3_handler'),
]
