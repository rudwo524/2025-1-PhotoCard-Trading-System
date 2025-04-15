from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.card_list, name = 'card_list'),
]