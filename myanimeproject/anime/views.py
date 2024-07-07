from django.shortcuts import render, redirect
from .models import Anime, User, Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm





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
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass

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