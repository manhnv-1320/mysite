from rest_framework.permissions import BasePermission


class CanMarkReturned(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('catalog.can_mark_returned')
