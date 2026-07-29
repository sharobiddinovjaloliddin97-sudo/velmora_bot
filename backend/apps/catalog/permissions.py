from rest_framework.permissions import BasePermission


class IsAdminOrEmployee(BasePermission):
    # DRF calls it before the view runs. built-in
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role in ["admin", "employee"] or request.user.is_superuser or request.user.is_staff)
        )

# Preventing access to a view means stopping a user from executing that API endpoint if they don't have permission.