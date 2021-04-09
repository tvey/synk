from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "Sorry, this link is not yours."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
