from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('riot-api-test/', views.riot_api_test, name='riot_api_test'),  # Ruta para la API
]
