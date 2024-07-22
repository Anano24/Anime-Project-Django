from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'


urlpatterns = [
    path('add_to_watchlist/<str:id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('delete_from_watchlist/<str:id>/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)