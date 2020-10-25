from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api-auth/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('Blog.urls')),
]
