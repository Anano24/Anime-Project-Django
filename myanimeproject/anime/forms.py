from .models import Anime
from django.forms import ModelForm

        
        
class AnimeAddForm(ModelForm):
    class Meta:
        model = Anime
        fields = '__all__'



