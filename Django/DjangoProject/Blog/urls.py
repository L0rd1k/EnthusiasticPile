from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name="category-overview"),
    path('category/<int:pk>', views.CategoryDetailView.as_view()),
    path('genre/', views.GenreListView.as_view()),
    path('genre/<int:pk>', views.GenreDetailView.as_view())
]