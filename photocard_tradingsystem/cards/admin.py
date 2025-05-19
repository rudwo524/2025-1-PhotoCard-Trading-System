from django.contrib import admin
from .models import Card, User, Trade, Category, Grade, CreatedCard, TradeRequest  # 만든 모델 이름

# Register your models here.
admin.site.register(Card) # 관리자 페이지에 Card 모델 등록
admin.site.register(User) # 관리자 페이지에 Card Instance 모델 등록
admin.site.register(Trade) # 관리자 페이지에 Trading 모델 등록
admin.site.register(Category)
admin.site.register(Grade)
admin.site.register(CreatedCard)
admin.site.register(TradeRequest)