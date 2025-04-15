from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


# 카드 기본 정보 (카드 마스터 데이터)
class CardMaster(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='cards/')
    grade = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name} ({self.grade})"

# 생성된 카드 (유저 소유 카드 인스턴스)
class CardInstance(models.Model):
    card = models.ForeignKey(CardMaster, on_delete=models.CASCADE, related_name='instances')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.card.name} - Owned by {self.owner.username}"


# 거래 정보 (히스토리 누적)
class Trade(models.Model):
    card_instance = models.ForeignKey(CardInstance, on_delete=models.CASCADE, related_name='trades')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    price = models.PositiveIntegerField()
    traded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_instance.card.name} | {self.seller.username} ➝ {self.buyer.username} | ₩{self.price}"

image = models.ImageField(upload_to='cards/')