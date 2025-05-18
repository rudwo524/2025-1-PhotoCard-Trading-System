from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

# # 카드 기본 정보 (카드 마스터 데이터)
# class CardMaster(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50)
#     description = models.TextField()
#     image = models.ImageField(upload_to='cards/')
#     grade = models.CharField(max_length=5)
#     def __str__(self):
#         return f"{self.name} ({self.grade})"

# # 생성된 카드 (유저 소유 카드 인스턴스)
# class CardInstance(models.Model):
#     card = models.ForeignKey(CardMaster, on_delete=models.CASCADE, related_name='instances')
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_cards')
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     def __str__(self):
#         return f"{self.card.name} - Owned by {self.owner.username}"

# # 거래 정보 (히스토리 누적)
# class Trade(models.Model):
#     card_instance = models.ForeignKey(CardInstance, on_delete=models.CASCADE, related_name='trades')
#     seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
#     price = models.PositiveIntegerField()
#     traded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.card_instance.card.name} | {self.seller.username} ➝ {self.buyer.username} | ₩{self.price}"
# image = models.ImageField(upload_to='cards/')

# 등급 (레어도)
class Grade(models.Model):
    name = models.CharField(max_length=50)
    #probability = models.FloatField()
    def __str__(self):
        return self.name

# 카드 카테고리
class Category(models.Model):
    name = models.CharField(max_length=50)
    Year = models.CharField(max_length=4)
    def __str__(self):
        return self.name

# 카드 정보 (기본 정보)
class Card(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    image_url = models.ImageField(upload_to='card_images/')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

# 사용자 (간단한 커스텀 유저)
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)  # user-id 역할
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, default='user')
    def __str__(self):
        return self.username

# 생성된 카드 (유저가 보유한 개별 카드 단위)
class CreatedCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    trade_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.card.name if self.card else '알 수 없음'} - {self.owner.username if self.owner else '소유자 없음'}"

# 거래 정보
# class Trade(models.Model):
#     created_card = models.ForeignKey(CreatedCard, on_delete=models.SET_NULL, null=True, blank=True)
#     seller = models.ForeignKey(User, related_name='sell_trades', on_delete=models.SET_NULL, null=True, blank=True)
#     buyer = models.ForeignKey(User, related_name='buy_trades', on_delete=models.SET_NULL, null=True, blank=True)
#     price = models.IntegerField()
#     traded_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         card_name = self.created_card.card.name if self.created_card and self.created_card.card else "카드 없음"
#         return f"{card_name} 거래 - {self.price}원"
# image = models.ImageField(upload_to='cards/')


# cards/models.py

class Trade(models.Model):
    created_card = models.ForeignKey(CreatedCard, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(User, related_name='sell_trades', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)  # 거래 진행 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_card.card.name} - {self.price}원"

class TradeRequest(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buy_requests', on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True)  # None: 대기, True: 승인, False: 거절
    requested_at = models.DateTimeField(auto_now_add=True)