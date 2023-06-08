#to create custom persmissions
from rest_framework.permissions import BasePermission,SAFE_METHODS

class ReadOnly(BasePermission):
    #it allows us to only access endpoints when we get information from the request itself 
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class AuthorOrReadonly(BasePermission):
    #This is because instead of depending on the request only we are going to depend both request information as well as the object we are trying to update/delete  
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return False
    
