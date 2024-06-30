from django.shortcuts import render
from .models import Anime, User
# Create your views here.




def home(request):
    anime_list = Anime.objects.all()
    context = {'anime_list': anime_list}

    return render(request, 'anime/home.html', context)


def profile(request, pk):
    user = User.objects.get(id=int(pk))
    animes = user.animes.all()
    context = {'anime_list': animes, 'user': user}
    return render(request, 'anime/profile.html', context)