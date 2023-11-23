from django.contrib import admin

from movie import models


admin.site.register(models.Actors)
admin.site.register(models.AgeLimits)
admin.site.register(models.Comments)
admin.site.register(models.Directors)
admin.site.register(models.Countries)
admin.site.register(models.Genres)
admin.site.register(models.Platform)
admin.site.register(models.MoviesInfo)
admin.site.register(models.SeriesInfo)
