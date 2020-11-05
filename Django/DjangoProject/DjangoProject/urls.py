from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('', include('Blog.urls')),
]
