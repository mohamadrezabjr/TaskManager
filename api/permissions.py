from rest_framework import permissions
from core.models import Project

class IsLeadPermission(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):

        try:
            return obj.is_lead(request.user)
        except:
            return super().has_object_permission()


    def has_permission(self, request, view):

        try:
            project_token = view.kwargs.get('token')
            project = Project.objects.get(token= project_token)
        except Project.DoesNotExist:
            return False
        return project.is_lead(request.user)

class IsAssistPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        try:
            return obj.is_assist(request.user)
        except:
            return super().has_object_permission()


    def has_permission(self, request, view):

        try:
            project_token = view.kwargs.get('token')
            project = Project.objects.get(token= project_token)
        except Project.DoesNotExist:
            return False
        return project.is_assist(request.user)

class IsMemberPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        try:
            return obj.is_member(request.user)
        except:
            project = obj.project

            return project.is_member(request.user)

