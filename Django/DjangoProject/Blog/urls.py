from django.urls import re_path, path, include
from . import views

from rest_framework.routers import DefaultRouter
from .views import ActorViewSet #ActorListView



# from .views import RegistrationAPIView
# from .views import LoginAPIView


router = DefaultRouter()
router.register(r'actor',ActorViewSet, basename='actor')



urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name="category-overview"),
    path('category/<int:pk>', views.CategoryDetailView.as_view()),

    path('genre/', views.GenreListView.as_view()),
    path('genre/<int:pk>', views.GenreDetailView.as_view()),


    path('movie-shot/', views.MovieShotListView),
    path('movie-shot/<int:pk>', views.MovieShotDetailListView),

    path('movie/', views.MovieListView.as_view()),
    path('movie/<int:pk>', views.MovieDetailView.as_view()),

    path("review/", views.ReviewCreateView.as_view()),


    # path("registration/", RegistrationAPIView.as_view(), name='user_registration'),
    # path("login/", LoginAPIView.as_view(), name='user_registration'),

    path('', include(router.urls))
]