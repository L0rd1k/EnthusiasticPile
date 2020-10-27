from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name="api-overview"),
    path('category/<int:pk>', views.CategoryDetailView.as_view())
]