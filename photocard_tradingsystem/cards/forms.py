from django import forms 
from .models import Card, Category, Grade

class CardForm(forms.ModelForm): 
    class Meta: 
        model = Card 
        fields = ['name', 'category', 'description', 'image_url', 'grade']

class CategoryForm(forms.ModelForm): 
    class Meta: 
        model = Category 
        fields = ['name', 'updated_at']

class GradeForm(forms.ModelForm): 
    class Meta: 
        model = Grade 
        fields = ['name', 'probability']