from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
#1 method
from rest_framework.views import APIView

# 2 method
from rest_framework.generics import GenericAPIView  # 2 method
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

#3 method
from rest_framework import viewsets

from .models import Category, Genre, Actor
from .serializers import CategorySerializer, GenreSerializer, ActorSerializer
from .serializers import CategoryDetailSerializer
#======================================================
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
