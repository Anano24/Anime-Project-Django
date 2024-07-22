from django.db import models
from users.models import User

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name



class LanguageOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    status = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    cover_image = models.ImageField(null=True, blank=True, upload_to='anime_cover_img/')
    subtitle_or_dub = models.ManyToManyField(LanguageOption, related_name='animes')

    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title
    

    def total_seasons(self):
        return self.seasons.count()

    def total_episodes(self):
        return sum(season.episodes.count() for season in self.seasons.all())
    


class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    release_date = models.DateField()

    def __str__(self):
        return f"{self.anime.title} - Season {self.season_number}"



class Episode(models.Model):
    
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    episode_number = models.PositiveIntegerField()
    summary = models.TextField()
    air_date = models.DateField()
    duration = models.DurationField()
    video_file = models.FileField(upload_to='anime_videos/')
    episod_cover_image = models.ImageField(null=True, blank=True, upload_to='episode_cover_img/')
    

    def __str__(self):
        return f"{self.season.anime.title} - Season {self.season.season_number} - Episode {self.episode_number}"
    





class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body