from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from anime.models import Anime, Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, UserForm
from django.contrib import messages




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
        
    context = {'anime_list': animes, 'user': user, 'genres': genres}
    return render(request, 'users/profile.html', context)



@login_required(login_url='login')
def add_to_watchlist(request, id):
    anime = Anime.objects.get(id=id)
    user = request.user
    user.animes.add(anime)
    return redirect('users:profile', user.id)



@login_required(login_url='login')
def delete_from_watchlist(request, id):
    anime = Anime.objects.get(id=id)

    if request.method == "POST":
        request.user.animes.remove(anime)
        return redirect('users:profile', request.user.id)
    
    return render(request, 'users/delete_confirm.html', {'obj': anime})




def login_page(request):
    genres = Genre.objects.all()
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
            return redirect('users:login')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('anime:home')
        else:
            messages.error(request, "Username or password is incorrect!")

    context = {'page': page, 'genres': genres}
    return render(request, 'users/login_register.html', context)




def logout_page(request):
    logout(request)
    return redirect('users:login')



def register_page(request):
    genres = Genre.objects.all()
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('anime:home')

    context = {'form': form, 'genres': genres}
    return render(request, 'users/login_register.html', context)



@login_required(login_url='login')
def update_profile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user.id)
    return render(request, 'users/update_profile.html', {'form': form})
