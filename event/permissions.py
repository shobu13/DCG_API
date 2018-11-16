from rest_framework import permissions


class IsEventOwner(permissions.BasePermission):
    message = 'You are not the owner of this event.'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print("test")

        return (request.user.is_authenticated and obj.owner == request.user) or request.user.is_superuser
