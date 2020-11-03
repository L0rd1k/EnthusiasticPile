from rest_framework.response import Response

from rest_framework import status
from rest_framework.generics import get_object_or_404

# Import our models (DB - tables)
from .models import Category 
from .models import Genre
from .models import Actor
from .models import MovieShots 
from .models import Movie

# Our serializers
from .serializers import CategorySerializer, CategoryDetailSerializer
from .serializers import GenreSerializer
from .serializers import ActorSerializer
from .serializers import MovieShotsSerializer
from .serializers import MovieListSerializer, MovieDetailSerializer
from .serializers import ReviewCreateSerializer


############# 1 method - Function Based Views #############
# Wrapping API views with DECORATORS
from rest_framework.decorators import api_view 
# "API policy decorators" - override the default settings
from rest_framework.decorators import throttle_classes
# "View schema decorator" - override the default schema generation for function based views
from rest_framework.decorators import schema 
###########################################################

############## 2 method - Class-based Views ###############
from rest_framework.views import APIView
###########################################################

############## 3 method - Generic views ##################
from rest_framework.generics import GenericAPIView
# Methods:
# 1. queryset            |  get_queryset(self)
# 2. lookup_field        |  get_object(self)
# 3. queryset            |  filter_queryset(self, queryset)
# 4. serializer_class    |  get_serializer_class(self)

############## Concrete View Classes ##################
from rest_framework.generics import CreateAPIView 
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView 
from rest_framework.generics import RetrieveUpdateAPIView 
from rest_framework.generics import RetrieveUpdateDestroyAPIView

############## Mixins ##################
# Methods .get() / .post()
from rest_framework.mixins import ListModelMixin        # .list(request, *args, **kwargs)
from rest_framework.mixins import CreateModelMixin      # .create(request, *args, **kwargs)
from rest_framework.mixins import RetrieveModelMixin    # .retrieve(request, *args, **kwargs)
from rest_framework.mixins import UpdateModelMixin      # .update(request, *args, **kwargs) / .partial_update(request, *args, **kwargs)
from rest_framework.mixins import DestroyModelMixin     # .destroy(request, *args, **kwargs)

# perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
# perform_update(self, serializer) - Called by UpdateModelMixin when saving an existing object instance.
# perform_destroy(self, instance) - Called by DestroyModelMixin when deleting an object instance.


###########################################################


############## 4 method - ViewSets ##################
from rest_framework import viewsets
# A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as .get() or .post(), and instead provides actions such as .list() and .create()


#===============================AUTH==========================================
# from rest_framework.permissions import AllowAny
# from .models import User
# from .serializers import LoginSerializer
# from .serializers import RegistrationSerializer




#======================================================================================
# 1.Set of simple decorators that wrap your function based views to ensure they receive an instance of 'Request' and allows them to return a 'Response', and allow you to configure how the request is processed.
# 2.api_view decorator takes a list of HTTP methods that your view should respond to.
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
# 1. 'APIView' class subclasses Django's 'View' class.
# 2. Requests passed to the handler methods will be 'Request' instance / not Django's HttpRequest instance
# 3. Handler methods may return REST framework's 'Response', instead of Django's 'HttpResponse'. 
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
# class RegistrationAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = RegistrationSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 'token': serializer.data.get('token', None),
#             },
#             status=status.HTTP_201_CREATED,
#         )

# class LoginAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)