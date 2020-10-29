from django.contrib import admin
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Review
# Register your models here.
#

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)

@admin.register(Actor)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "image")
    list_display_links = ("name",)

@admin.register(Genre)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url")
    list_display_links = ("name",)

@admin.register(Movie)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", 
                    "tagline", 
                    "description", 
                    "poster", 
                    "year",
                    "country",
                    #"get_director",
                    #"actors",
                    #"genres",
                    "world_premiere",
                    "budget",
                    "fees_in_usa",
                    "fess_in_world",
                    "category",
                    "url",
                    "draft")
    def get_director(self, obj):
        return "\n".join([d.directors for d in obj.directors.all()])
    #list_display_links = ("get_director", )


@admin.register(MovieShots)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    list_display_links = ("title",)