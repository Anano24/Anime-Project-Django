from django.db import models

# Create your models here.



class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    episodes = models.PositiveIntegerField()
    status = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    cover_image = models.CharField(max_length=300)

    def __str__(self):
        return self.title