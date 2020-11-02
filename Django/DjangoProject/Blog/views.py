from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Category, Genre, Actor, MovieShots, Movie
from .serializers import CategorySerializer, GenreSerializer, ActorSerializer, MovieShotsSerializer, MovieListSerializer, ReviewCreateSerializer
from .serializers import CategoryDetailSerializer, MovieDetailSerializer

#wrapping API views with decorator
from rest_framework.decorators import api_view
from rest_framework import status

#1 method
from rest_framework.views import APIView

# 2 method
from rest_framework.generics import GenericAPIView  # 2 method
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

#3 method
from rest_framework import viewsets
#======AUTH==========================================
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer

#======================================================================================

#======================================================================================
@api_view(['GET', 'POST'])
def MovieShotListView(request):
    if request.method == 'GET':
        movieshot = MovieShots.objects.all()    
        serializer = MovieShotsSerializer(movieshot, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieShotsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def MovieShotDetailListView(request, pk):
    try:
        movieShot = MovieShots.objects.get(pk=pk)
    except MovieShots.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MovieShotsSerializer(movieShot)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieShotsSerializer(movieShot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movieShot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#======================================================================================

#======================================================================================
class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        saved_category = get_object_or_404(Category.objects.all(), pk=pk)
        data = request.data.get('category')
        serializer = CategoryDetailSerializer(instance=saved_category, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()
            return Response({"success": "Category '{}' updated successfully".format(category_saved.name)})

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.all(), pk=pk)
        category.delete()
        return Response({
            "message": "Category `{}` has been deleted.".format(category.name)
        }, status=204)


class CategoryListView(APIView):
    def get(self,request):
        category = Category.objects.all()
        # many - означает, что сериализатор будет сериализовывать более одной категории
        serializer = CategorySerializer(category, many=True)
        return Response({"category" : serializer.data})

    def post(self, request):
        category = request.data.get('category')
        serializer = CategorySerializer(data=category)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()
        return Response({"success":"Category '{}' created successfully".format(category_saved.name)})

#======================================================================================

#======================================================================================
#class GenreListView(ListModelMixin, CreateModelMixin, GenericAPIView):
class GenreListView(CreateAPIView, ListAPIView):
    queryset = Genre.objects.all() #  # (запрос к базе) который используется для получение объектов.
    serializer_class = GenreSerializer # класс сериализатора, который используется для проверки и десериализации объектов из базы
    # get_queryset - запрос с фильтрацией
    def perform_create(self, serializer):
        # genre = get_object_or_404(Genre, name=self.request.data.get('name'))
        return serializer.save()
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

class GenreDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

#======================================================================================

#======================================================================================
class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


# class ActorListView(viewsets.ViewSet):
    # def list(self, request):
    #     queryset = Actor.objects.all()
    #     serializer = ActorSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     queryset = Actor.objects.all()
    #     actor = get_object_or_404(queryset,pk=pk)
    #     serializer = ActorSerializer(actor)
    #     return Response(serializer.data)
#======================================================================================

#======================================================================================

class MovieListView(APIView):
    def get(self, request):
        movies =  Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)



class MovieDetailView(APIView):
    def get(self, request, pk):
        movie =  Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

#======================================================================================

#======================================================================================

class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


#======================================================================================

#======================================================================================
class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)