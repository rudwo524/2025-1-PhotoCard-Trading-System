from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.card_list, name = 'card_list'),
    path('add/', views.add_card, name='add_card'), # 예: path('', views.card_list, name='card_list') 도 함께 작성 예정
    path('<int:pk>/', views.card_detail, name='card_detail'),            # 상세 보기
    path('<int:pk>/edit/', views.update_card, name='update_card'),      # 수정
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('grades/', views.grade_list, name='grades'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/<int:pk>/edit/', views.update_grade, name='update_grade'),
    path('grades/<int:pk>/delete/', views.delete_grade, name='delete_grade'),
    
]