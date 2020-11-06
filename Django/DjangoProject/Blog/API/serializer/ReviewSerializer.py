from rest_framework import serializers
from Blog.models import Review
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
