from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('add_to_watchlist/<str:id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('delete_from_watchlist/<str:id>/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('add/', views.add_anime, name='add'),
    path('detailed_anime/<str:id>/', views.detailed_anime, name='detailed_anime'),
    path('detailed_anime/<str:anime_id>/season/<str:season_id>/episode/<str:episode_id>/', views.episode_detail, name='episode_detail'),
    path('get_episodes/<int:anime_id>/season/<int:season_id>/', views.get_episodes, name='get_episodes'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)