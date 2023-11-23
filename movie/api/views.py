from rest_framework.generics import ListAPIView

from movie.api import serializers
from movie import models


class MoviesListAV(ListAPIView):
    queryset = models.MoviesInfo.objects.all()
    serializer_class = serializers.MoviesListSerializer

