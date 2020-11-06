from django.urls import re_path, path, include

from rest_framework.routers import DefaultRouter


from .API.views import AuthView
from .API.views import MovieShotView
from .API.views import CategoryView
from .API.views import GenreView
from .API.views import ActorView
from .API.views import MovieView
from .API.views import ReviewView

from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'actor', ActorView.ActorViewSet, basename='actor')


urlpatterns = [
    path('category/', CategoryView.CategoryListView.as_view(), name="category-overview"),
    path('category/<int:pk>', CategoryView.CategoryDetailView.as_view()),

    path('genre/', GenreView.GenreListView.as_view()),
    path('genre/<int:pk>', GenreView.GenreDetailView.as_view()),

    path('movie-shot/', MovieShotView.MovieShotListView),
    path('movie-shot/<int:pk>', MovieShotView.MovieShotDetailListView),

    path('movie/', MovieView.MovieListView.as_view()),
    path('movie/<int:pk>', MovieView.MovieDetailView.as_view()),

    path("review/", ReviewView.ReviewCreateView.as_view()),


    path("api-token-user/", AuthView.UserCreate.as_view(), name="user_create"),
    path("api-token-auth/", obtain_auth_token, name="login"),



    path('', include(router.urls))
]