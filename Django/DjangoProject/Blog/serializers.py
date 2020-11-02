from rest_framework import serializers
from .models import Category, Genre, Actor, MovieShots, Movie, Review
# from .models import User

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


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "tagline")

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewCreateSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ("draft",)


# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField( max_length=128, min_length=8, write_only=True,)
#     token = serializers.CharField(max_length=255, read_only=True)

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password', 'token',)

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(write_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)
#     username = serializers.CharField(max_length=255, read_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)

#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)
#         if email is None:
#             raise serializers.ValidationError( 'An email address is required to log in.')

#         if password is None:
#             raise serializers.ValidationError('A password is required to log in.')
        
#         user = authenticate(username=email, password=password)
        
#         if user is None:
#             raise serializers.ValidationError('A user with this email and password was not found.')
#         if not user.is_active:
#             raise serializers.ValidationError('This user has been deactivated.')
        
#         return { 'token': user.token, }

#     class Meta:
#         model = User
#         fields = ("username",)
