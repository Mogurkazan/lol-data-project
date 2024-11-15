from django.urls import path
from . import views

urlpatterns = [
    path('', views.champions_list, name='champions_list'),
    path('champions/<str:champion_id>/', views.champion_detail, name='champion_detail'),
]
