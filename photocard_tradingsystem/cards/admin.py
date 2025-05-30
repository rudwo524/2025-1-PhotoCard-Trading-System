from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Card, User, Trade, Category, Grade, CreatedCard, TradeRequest  # 만든 모델 이름


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'name', 'is_staff', 'is_superuser']
    fieldsets = [
        (None, {'fields': ('username', 'name', 'password')}),
        ('Permissions', {'fields': ( 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Permissions', {'fields': ('is_activate', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'password1', 'password2', 'is_staff', 'is_superuser')
        })
    ]
    search_fields = ('username',)
    ordering = ('username',)


# Register your models here.
admin.site.register(Card) # 관리자 페이지에 Card 모델 등록
admin.site.register(User, UserAdmin) # 관리자 페이지에 Card Instance 모델 등록
admin.site.register(Trade) # 관리자 페이지에 Trading 모델 등록
admin.site.register(Category)
admin.site.register(Grade)
admin.site.register(CreatedCard)
admin.site.register(TradeRequest)