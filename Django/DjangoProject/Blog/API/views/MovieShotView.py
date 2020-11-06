############# 1 method - Function Based Views #############
# Wrapping API views with DECORATORS
from rest_framework.decorators import api_view 
# "API policy decorators" - override the default settings
from rest_framework.decorators import throttle_classes
# "View schema decorator" - override the default schema generation for function based views
from rest_framework.decorators import schema 
###########################################################
from rest_framework.response import Response
from rest_framework import status
from Blog.models import MovieShots 

from Blog.API.serializer.MovieShotSerializer import  MovieShotsSerializer

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