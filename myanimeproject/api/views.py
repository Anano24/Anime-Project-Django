from rest_framework.response import Response
from rest_framework.decorators import api_view
from anime.models import Anime
from .serializers import AnimeSerializer

# Create your views here.


@api_view(['GET'])
def get_routes(request):
    routes = [
        "GET /api",
        "GET /api/animes",
        "GET /api/anime/:id"
    ]
    return Response(routes)



@api_view(['GET'])
def get_animes(request):
    animes = Anime.objects.all()
    serializer = AnimeSerializer(animes, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_anime(request, id):
    anime = Anime.objects.get(id=id)
    serializer = AnimeSerializer(anime, many=False)
    return Response(serializer.data)