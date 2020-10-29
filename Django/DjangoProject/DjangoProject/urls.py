from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Blog.urls')),
    path('api-auth/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('Blog.urls')),
]
