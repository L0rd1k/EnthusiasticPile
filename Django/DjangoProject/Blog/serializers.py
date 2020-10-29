from rest_framework import serializers
from .models import Category, Genre, Actor, MovieShots

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'url')


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



#сождержит в себе методы update и create
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'description',
            'url')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieShots
        fields = '__all__'
