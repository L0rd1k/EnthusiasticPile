from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .views import ActorViewSet #ActorListView

router = DefaultRouter()
router.register(r'actor',ActorViewSet, basename='actor')



urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name="category-overview"),
    path('category/<int:pk>', views.CategoryDetailView.as_view()),

    path('genre/', views.GenreListView.as_view()),
    path('genre/<int:pk>', views.GenreDetailView.as_view()),

    path('', include(router.urls))
]