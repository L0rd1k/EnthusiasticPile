from rest_framework import serializers
from Blog.models import Genre

#сождержит в себе методы update и create
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'description',
            'url')