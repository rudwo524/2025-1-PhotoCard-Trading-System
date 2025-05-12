# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Card, Category, Grade, User, CreatedCard
from .forms import CardForm, CategoryForm, GradeForm, DrawCardForm, CreatedCard
import os
from django.conf import settings
import random
from django.db.models import Q
from django.contrib.auth.models import User

def card_list(request):
    cards = Card.objects.all()
    image_dir = os.path.join(settings.MEDIA_ROOT, 'cards')
    try:
        image_filenames = os.listdir(image_dir)
        image_urls = ['/media/cards/' + filename for filename in image_filenames]
    except FileNotFoundError:
        image_urls = []
    print(image_urls)
    return render(request, 'cards/card_list.html', {'cards': cards})

    
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
    else:
        form = CardForm() 
    if form.is_valid():
        form.save()
        # 이전 페이지로 리디렉션
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else 'card_list')
    else:
        form = CardForm()
    return render(request, 'cards/card_form.html', {'form': form})
    # form = CardForm()
    # return render(request, 'cards/add_cards.html', {'form': form}) # 카드 리스트 페이지로 리디렉션 else: form = CardForm() return render(request, 'cards/add_card.html', {'form': form})

# 카드 상세 페이지
def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, 'cards/card_detail.html', {'card': card})

# 카드 수정
def update_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('card_detail', pk=card.pk)
    else:
        form = CardForm(instance=card)
    return render(request, 'cards/card_form.html', {'form': form, 'card': card})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')  # 등록 후 목록 페이지로 리디렉션
    else:
        form = CategoryForm()
    return render(request, 'cards/add_categories.html', {'form': form}) 

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'cards/category_list.html', {'categories': categories})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'cards/category_update.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'cards/category_confirm_delete.html', {'category': category})

def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'cards/grade_list.html', {'grades': grades})

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm()
    return render(request, 'cards/grade_form.html', {'form': form})

def update_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'cards/grade_form.html', {'form': form})

def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grades')
    return render(request, 'cards/confirm_delete_grade.html', {'grade': grade})

# def draw_card(request):
#     cards = Card.objects.all()
#     if cards.exists():
#         card = random.choice(cards)
#     else:
#         card = None
#     return render(request, 'cards/draw_card.html', {'card': card})


# def draw_card(request):

#     card = None
#     if request.method == 'POST':
#         form = DrawCardForm(request.POST)
#         if form.is_valid():
#             card = random.choice(Card.objects.all())
#             CreatedCard.objects.create(user = request.user, card = card)
#     else:
#         form = DrawCardForm()
#     return render(request, 'cards/draw_card.html', {'form': form, 'card': card})

# def draw_card(request):
#     card = None
#     cards = Card.objects.all()
#     users = User.objects.all()
#     if cards.exists():
#         card = random.choice(cards)
#         form = DrawCardForm()
#     else:
#         form = None
#     return render(request, 'cards/draw_card.html', {'form': form, 'card': card, 'users':users})

def draw_card(request):

    users = User.objects.all()
    card = None
    selected_user_id = None

    if request.method == 'POST':
        form = DrawCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('draw_card')
    else:
        # 랜덤 카드 선택
        card = random.choice(Card.objects.all())
        form = DrawCardForm(initial={'card': card})

        # 유저 전체 목록 (드롭다운용)
    users = User.objects.all()

    # 선택된 유저의 카드 목록 조회
    if not selected_user_id:
        selected_user_id = form.initial.get('owner') or users.first().id
    my_cards = CreatedCard.objects.filter(owner_id=selected_user_id).select_related('card')

    return render(request, 'cards/draw_card.html', {
        'form': form,
        'card': card,
        'my_cards': my_cards,
        'users': users
    })

def manage_cards(request):
    cards = CreatedCard.objects.all()   # foreignkey로 설정해놔서 다 받아와짐
   
    selected_grade = request.GET.get('grade')
    selected_category = request.GET.get('category')
    selected_owner = request.GET.get('owner')
    selected_date = request.GET.get('date')
    sort_option = request.GET.get('sort')

    if selected_grade:
        cards = cards.filter(card__grade__id=selected_grade)
    if selected_category:
        cards = cards.filter(card__category__id=selected_category)
    if selected_owner:
        cards = cards.filter(card__owner__id=selected_owner)
    if selected_date:
        cards = cards.filter(created_at__date=selected_date)
    
    if sort_option == 'name':
        cards = cards.order_by('card__name')
    elif sort_option == 'grade':
        cards = cards.order_by('card__grade__name')
    else:
        cards = cards.order_by('created_at')

    context = {
        'cards': cards,
        'grades':Grade.objects.all(),
        'categories': Category.objects.all(),
        'owners': User.objects.all(),
        'selected_grade': selected_grade,
        'selected_category': selected_category,
        'selected_owner': selected_owner,
        'selected_date' : selected_date,
        'sort_option': sort_option
    }
    return render(request,'cards/manage.html',
                  context
                  )







    
