from django.shortcuts import render
from .models import Anime, User, Genre
from django.db.models import Q
# Create your views here.




def home(request):
    query = request.GET.get("query")
    genres = Genre.objects.all()

    if query:
        anime_list = Anime.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(genres__name__icontains=query))
        anime_list = list(set(anime_list))
    else:
        anime_list = Anime.objects.all()

    heading = "All Animes"
    context = {'anime_list': anime_list, 'heading': heading, 'genres': genres}

    return render(request, 'anime/home.html', context)



def profile(request, pk):
    user = User.objects.get(id=int(pk))
    query = request.GET.get("query")
    genres = Genre.objects.all()

    if query:
        animes = user.animes.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(genres__name__icontains=query))
        animes= list(set(animes))
    else:
        animes = user.animes.all()
        
    heading = "My Animes"
    context = {'anime_list': animes, 'user': user, 'heading': heading, 'genres': genres}
    return render(request, 'anime/profile.html', context)