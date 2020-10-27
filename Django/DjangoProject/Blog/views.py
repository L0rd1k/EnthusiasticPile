from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer

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