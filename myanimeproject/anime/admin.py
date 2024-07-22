from django.contrib import admin
from .models import Anime, Genre, Season, Episode, LanguageOption, Comment


# Register your models here.


admin.site.register(Genre)
admin.site.register(LanguageOption)
admin.site.register(Anime)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Comment)