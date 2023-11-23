from rest_framework import serializers

from movie import models

class MoviesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MoviesInfo
        fields = "__all__"
