from django import forms 
from .models import Card, Category, Grade

class CardForm(forms.ModelForm): 
    class Meta: 
        model = Card 
        fields = ['name', 'category', 'description', 'image_url', 'grade']

class CategoryForm(forms.ModelForm): 
    class Meta: 
        model = Category 
        fields = ['name', 'Year']

class GradeForm(forms.ModelForm): 
    class Meta: 
        model = Grade 
        fields = ['name', 'probability']


# created_at, delete_at, update_at