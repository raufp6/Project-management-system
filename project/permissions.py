from rest_framework import permissions

class IsStaffPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    # def has_permission(self, request, view):
    #     user = request.user
    #     print(user.get_all_permissions())
    #     if user.is_staff:
    #         if user.has_perm("project.add_projects"):
    #             return True
    #         if user.has_perm("project.delete_projects"):
    #             return True
    #         if user.has_perm("project.change_projects"):
    #             return True
    #         if user.has_perm("project.view_projects"):
    #             return True
    #         return False
        
    #     return False
    