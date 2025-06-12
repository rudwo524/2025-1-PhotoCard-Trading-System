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
    # path('draw/', views.draw_card, name='draw_card'),
    path('manage/', views.manage_cards, name='manage_cards'),
    path('trades/', views.trade_list, name='trade_list'),
    path('trades/sell/', views.trade_create, name='trade_create'),
    path('trades/<int:trade_id>/request/', views.trade_request, name='trade_request'),
    path('trades/requests/', views.trade_requests_received, name='trade_requests_received'),
    path('trades/request/<int:req_id>/approve/', views.trade_approve, name='trade_approve'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('trading/', views.trading, name='trading'),
    # 📌 로그인한 유저용 뽑기 (자기 계정으로만)
    path('draw/', views.draw_card, name='draw_card'),

    # 📌 관리자용 뽑기 (다른 유저 골라서 발급)
    path('admin/draw/', views.draw_card_admin, name='draw_card_admin'),
]