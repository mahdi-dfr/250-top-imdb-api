from django.urls import path

from movie.api import views

urlpatterns = [
    path("movies-list/", views.MoviesListAV.as_view(), name="movies_list"),
]
