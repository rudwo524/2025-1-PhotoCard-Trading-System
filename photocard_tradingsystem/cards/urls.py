from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.card_list, name = 'card_list'),
    path('add/', views.add_card, name='add_card'), # 예: path('', views.card_list, name='card_list') 도 함께 작성 예정
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='category_list'),
]