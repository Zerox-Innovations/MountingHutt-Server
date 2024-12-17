from rest_framework import permissions



class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow only staff users (admins)
        return request.user.is_staff
