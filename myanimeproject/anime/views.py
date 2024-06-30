from django.shortcuts import render
from .models import Anime
# Create your views here.




def home(request):
    anime_list = Anime.objects.all()
    context = {'anime_list': anime_list}

    return render(request, 'anime/home.html', context)