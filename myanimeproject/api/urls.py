from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'api'


urlpatterns = [
    path('', views.get_routes),
    path('animes/', views.get_animes),
    path('anime/<str:id>', views.get_anime)
    

]

