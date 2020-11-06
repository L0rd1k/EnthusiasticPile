from rest_framework import viewsets
from Blog.models import Actor

from Blog.API.serializer.ActorSerializer import ActorSerializer

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

