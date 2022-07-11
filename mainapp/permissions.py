from rest_framework import permissions

class DontCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return False
        return bool(request.user or request.user.is_staff)
