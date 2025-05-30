from django import forms 
from .models import Card, Category, Grade, CreatedCard
from django.contrib.auth.forms import AuthenticationForm

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
        fields = ['name'] #, 'probability']

class DrawCardForm(forms.ModelForm):
    class Meta:
        model = CreatedCard
        fields = ['card', 'owner', 'trade_info'] #, 'created_at', 'deleted_at']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)
# created_at, delete_at, update_at