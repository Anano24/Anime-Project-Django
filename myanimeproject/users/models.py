from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    animes = models.ManyToManyField('anime.Anime', blank=True, related_name='users')
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='blank-profile-picture-973460_1280.png', upload_to='profile_img/')
