from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta del administrador
    path('', include('champions.urls')),  # Incluye las URLs de la app 'champions'
]
