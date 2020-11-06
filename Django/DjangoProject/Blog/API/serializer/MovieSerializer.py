from rest_framework import serializers
from Blog.models import Movie

from Blog.API.serializer.ReviewSerializer import ReviewCreateSerializer

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "tagline")

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewCreateSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ("draft",)