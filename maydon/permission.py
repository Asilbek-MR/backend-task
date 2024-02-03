from rest_framework import permissions

class CustomFieldPermission(permissions.BasePermission):
  

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, "profileuser"):
            role = user.profileuser.role
            if role == "admin":
                return True
            elif role == "field_owner" and obj.owner == user:
                return True
        return False



#fieldowner pass
#fieldowner


#asilbek99 pass
#oddiy

#asus123123
#asustime


