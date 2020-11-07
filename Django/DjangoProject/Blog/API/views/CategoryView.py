
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
#from rest_framework import permissions
from Blog.models import Category 
from Blog.permissions import IsAuthorOrReadOnly
from Blog.API.serializer.CategorySerializer import CategoryDetailSerializer
from Blog.API.serializer.CategorySerializer import CategorySerializer

class CategoryDetailView(APIView):
    # permission_classes = (permissions.IsAuthenticated, )
    # permission_classes = (IsAuthorOrReadOnly,)
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
    # permission_classes = (permissions.IsAuthenticated, )
    
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