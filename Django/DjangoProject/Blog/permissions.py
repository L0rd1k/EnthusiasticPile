from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS: # Если кортеж содержит GET, OPTIONS и HEAD, - тогда это запрос только для чтения, и разрешение предоставляется. 
            return True
        # Write permissions are only allowed to the author of a post
        return obj.user == request.user