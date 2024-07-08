from django.contrib.auth.forms import UserCreationForm
from .models import User, Anime
from django.forms import ModelForm
from django import forms



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

        
        
class AnimeAddForm(ModelForm):
    class Meta:
        model = Anime
        fields = '__all__'

