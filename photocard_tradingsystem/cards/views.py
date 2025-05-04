# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Card, Category, Grade
from .forms import CardForm, CategoryForm, GradeForm
import os
from django.conf import settings

def card_list(request):
    cards = Card.objects.all()
    # image_dir = os.path.join(settings.MEDIA_ROOT, 'cards')
    # try:
    #     image_filenames = os.listdir(image_dir)
    #     image_urls = ['/media/cards/' + filename for filename in image_filenames]
    # except FileNotFoundError:
    #     image_urls = []
    # print(image_urls)
    return render(request, 'cards/card_list.html', {'cards': cards})

    
def add_card(request):
    # if request.method == 'POST':
    #     form = CardForm(request.POST, request.FILES)
    # else:
    #     form = CardForm() 
    # if form.is_valid():
    #     form.save()
    form = CardForm()
    return render(request, 'cards/add_cards.html', {'form': form}) # 카드 리스트 페이지로 리디렉션 else: form = CardForm() return render(request, 'cards/add_card.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # 등록 후 목록 페이지로 리디렉션
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
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})