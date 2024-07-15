from django.shortcuts import render, redirect, get_object_or_404
from .models import Anime, User, Genre, LanguageOption, Episode, Season
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, AnimeAddForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages





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


@login_required(login_url='login')
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


@login_required(login_url='login')
def add_to_watchlist(request, id):
    anime = Anime.objects.get(id=id)
    user = request.user
    user.animes.add(anime)
    return redirect('profile', user.id)


@login_required(login_url='login')
def delete_from_watchlist(request, id):
    anime = Anime.objects.get(id=id)

    if request.method == "POST":
        request.user.animes.remove(anime)
        return redirect('profile', request.user.id)
    
    return render(request, 'anime/delete_from_watchlist.html', {'anime': anime})



def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist!")
            return redirect('login')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect!")

    context = {'page': page}
    return render(request, 'anime/login_register.html', context)




def logout_page(request):
    logout(request)
    return redirect('login')



def register_page(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'anime/login_register.html', context)



def add_anime(request):
    form = AnimeAddForm()
    genres = Genre.objects.all()
    subtitle_or_dub = LanguageOption.objects.all()

    if request.method == 'POST':
        anime_genre = request.POST.get('genre')
        anime_languageoption = request.POST.get('subtitle-or-dub')

        genre, created = Genre.objects.get_or_create(name=anime_genre)
        languageoption, created = LanguageOption.objects.get_or_create(name=anime_languageoption)

        form = AnimeAddForm(request.POST)

        new_anime = Anime(cover_image=request.FILES['cover_image'], title=form.data['title'], 
                          description=form.data['description'], 
                          release_date=form.data['release_date'], status=form.data['status'], 
                          rating=form.data['rating'])
        
        new_anime.save()
        new_anime.genres.add(genre)
        new_anime.subtitle_or_dub.add(languageoption)

        return redirect('home')
    
    context = {'form': form, 'genres': genres, 'subtitle_or_dub': subtitle_or_dub}
    return render(request, 'anime/add_anime.html', context)



def detailed_anime(request, id, season_id=None):
    anime = Anime.objects.get(id=id)
    seasons = anime.seasons.all()

    if season_id:
        season = get_object_or_404(Season, id=season_id, anime=anime)
    else:
        season = seasons.first()


    context = {'anime': anime, 'seasons': seasons, 'season': season}
    return render(request, 'anime/detailed_anime.html', context)


def episode_detail(request, anime_id, season_id, episode_id):
    anime = get_object_or_404(Anime, id=anime_id)
    season = get_object_or_404(Season, id=season_id, anime=anime)
    episode = get_object_or_404(Episode, id=episode_id, season=season)
    seasons = anime.seasons.all()

    context = {'anime': anime, 'season': season, 'episode':episode, 'seasons': seasons}
    return render(request, 'anime/episode_detail.html', context)


def get_episodes(request, anime_id, season_id):
    anime = get_object_or_404(Anime, id=anime_id)
    season = get_object_or_404(Season, id=season_id, anime=anime)
    episodes = season.episodes.all()

    html = render_to_string('anime/episode_list.html', {'episodes': episodes})
    return JsonResponse({'html': html})