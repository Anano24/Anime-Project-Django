from django.shortcuts import render, redirect, get_object_or_404
from .models import Anime, Genre, LanguageOption, Episode, Season, Comment
from users.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import AnimeAddForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator





def home(request):
    anime_list = Anime.objects.all()
    genres = Genre.objects.all()
    popular_animes = Anime.objects.filter(rating__gte=4.5)  # Adjust the rating threshold as needed
    heading = "Most Popular"
    context = {'anime_list': anime_list, 'genres': genres, 'heading':heading, 'popular_animes': popular_animes}
    return render(request, 'anime/home.html', context)



def search_results(request):
    query = request.GET.get("query")
    genres = Genre.objects.all()
    genre_name = request.GET.get("genre")
    
    if query:
        anime_list = Anime.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(genres__name__icontains=query))
        anime_list = list(set(anime_list))
    elif genre_name:
        anime_list = Anime.objects.filter(genres__name=genre_name)
    else:
        anime_list = Anime.objects.all()


    paginator = Paginator(anime_list, 4)
    page_number = request.GET.get('page')
    anime_list = paginator.get_page(page_number)

    heading = "Search results"
    context = {'anime_list': anime_list, 'genres': genres, 'heading': heading}

    return render(request, 'anime/search_results.html', context)



def all_anime(request):
    anime_list = Anime.objects.all()
    genres = Genre.objects.all()

    paginator = Paginator(anime_list, 6)
    page_number = request.GET.get('page')
    anime_list = paginator.get_page(page_number)

    heading = "All Anime"
    context = {'anime_list': anime_list, 'heading': heading, 'genres': genres}

    return render(request, 'anime/all_anime.html', context)



@login_required(login_url='login')
def delete_anime(request, id):
    anime = Anime.objects.get(id=id)
    
    if request.method == "POST":
        anime.cover_image.delete()
        anime.delete()
        return redirect('anime:home')
    return render(request, 'anime/delete_confirm.html', {'obj': anime})



@login_required(login_url='login')
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

        return redirect('anime:home')
    
    context = {'form': form, 'genres': genres, 'subtitle_or_dub': subtitle_or_dub}
    return render(request, 'anime/add_anime.html', context)



def detailed_anime(request, id, season_id=None):
    genres = Genre.objects.all()
    anime = Anime.objects.get(id=id)
    seasons = anime.seasons.all()
    anime_comments = anime.comment_set.all().order_by('-created')

    if season_id:
        season = get_object_or_404(Season, id=season_id, anime=anime)
    else:
        season = seasons.first()

    
    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            anime = anime,
            body = request.POST.get('body')
        )
        return redirect('anime:detailed_anime', id=id)  # Redirect after POST


    context = {'anime': anime, 'seasons': seasons, 'season': season, 'comments': anime_comments, 'genres': genres}
    return render(request, 'anime/detailed_anime.html', context)


def episode_detail(request, anime_id, season_id, episode_id):
    genres = Genre.objects.all()
    anime = get_object_or_404(Anime, id=anime_id)
    season = get_object_or_404(Season, id=season_id, anime=anime)
    episode = get_object_or_404(Episode, id=episode_id, season=season)
    seasons = anime.seasons.all()

    context = {'anime': anime, 'season': season, 'episode':episode, 'seasons': seasons, 'genres':genres}
    return render(request, 'anime/episode_detail.html', context)



@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    anime = comment.anime
    
    if request.method == 'POST':
        comment.delete()
        return redirect('anime:detailed_anime', anime.id)
    return render(request, 'anime/delete_confirm.html', {'obj': comment})



def get_episodes(request, anime_id, season_id):
    anime = get_object_or_404(Anime, id=anime_id)
    season = get_object_or_404(Season, id=season_id, anime=anime)
    episodes = season.episodes.all()

    html = render_to_string('anime/episode_list.html', {'episodes': episodes})
    return JsonResponse({'html': html})


