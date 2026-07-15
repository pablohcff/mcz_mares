from django.urls import path

from . import views

urlpatterns = [
    path("", views.extrair_dados, name="extrair_dados")
]
