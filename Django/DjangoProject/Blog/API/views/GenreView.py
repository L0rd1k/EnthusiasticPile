
from Blog.models import Genre
from Blog.API.serializer.GenreSerializer import GenreSerializer

############## 3 method - Generic views ##################
from rest_framework.generics import GenericAPIView
# ~~~ Methods ~~~ :
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
# ~~~ Methods ~~~ : .get() / .post()
from rest_framework.mixins import ListModelMixin        # .list(request, *args, **kwargs)
from rest_framework.mixins import CreateModelMixin      # .create(request, *args, **kwargs)
from rest_framework.mixins import RetrieveModelMixin    # .retrieve(request, *args, **kwargs)
from rest_framework.mixins import UpdateModelMixin      # .update(request, *args, **kwargs) / .partial_update(request, *args, **kwargs)
from rest_framework.mixins import DestroyModelMixin     # .destroy(request, *args, **kwargs)

# perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
# perform_update(self, serializer) - Called by UpdateModelMixin when saving an existing object instance.
# perform_destroy(self, instance) - Called by DestroyModelMixin when deleting an object instance.
###########################################################

#class GenreListView(ListModelMixin, CreateModelMixin, GenericAPIView):
class GenreListView(CreateAPIView, ListAPIView):
    queryset = Genre.objects.all() #  # (запрос к базе) который используется для получение объектов.
    serializer_class = GenreSerializer # класс сериализатора, который используется для проверки и десериализации объектов из базы
    # # get_queryset - запрос с фильтрацией
    # def perform_create(self, serializer):
    #     # genre = get_object_or_404(Genre, name=self.request.data.get('name'))
    #     return serializer.save()
    # # def get(self, request, *args, **kwargs):
    # #     return self.list(request, *args, **kwargs)
    # # def post(self, request, *args, **kwargs):
    # #     return self.create(request, *args, **kwargs)

class GenreDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer