import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photocard_tradingsystem.settings")
django.setup()

from cards.models import CardMaster

CardMaster.objects.create(
    name='팔단관',
    category='학교',
    description='소프트웨어 공학부 학과 건물입니다.',
    image='cards/팔단관.jpg',
    grade='3등급'
)
print("카드 등록 완료!")