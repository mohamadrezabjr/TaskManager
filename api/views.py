from django.shortcuts import render
from rest_framework import generics
from core.models import *
from .serializers import  *
class ProjectList(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def perform_create(self, serializer):
        serializer.save(lead = self.request.user)

    def get_queryset(self, *args, **kwargs):

        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user

        return qs.filter(lead = user)

class CreateUser(generics.CreateAPIView):

    model = User
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []

#
# class Project
# # Create your views here.
