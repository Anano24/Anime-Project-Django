from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'anime'


urlpatterns = [
    path('', views.home, name='home'),
    path('all_anime', views.all_anime, name='all_anime'),
    path('search/', views.search_results, name='search_results'),
    path('add/', views.add_anime, name='add'),
    path('detailed_anime/<str:id>/', views.detailed_anime, name='detailed_anime'),
    path('detailed_anime/<str:anime_id>/season/<str:season_id>/episode/<str:episode_id>/', views.episode_detail, name='episode_detail'),
    path('get_episodes/<int:anime_id>/season/<int:season_id>/', views.get_episodes, name='get_episodes'),
    path('delete_anime/<str:id>/', views.delete_anime, name='delete_anime'),
    path('delete_comment/<str:comment_id>/', views.delete_comment, name='delete_comment'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)