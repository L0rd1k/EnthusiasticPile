from rest_framework import serializers
from Blog.models import MovieShots

class MovieShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieShots
        fields = '__all__'