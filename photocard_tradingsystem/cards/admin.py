from django.contrib import admin
from .models import CardMaster, CardInstance, Trade   # 만든 모델 이름

# Register your models here.
admin.site.register(CardMaster) # 관리자 페이지에 모델 등록
admin.site.register(CardInstance) # 관리자 페이지에 모델 등록
admin.site.register(Trade) # 관리자 페이지에 모델 등록
