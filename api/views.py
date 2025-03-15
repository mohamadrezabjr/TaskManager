
from django.shortcuts import render
from rest_framework import generics, mixins
from core.models import *
from .serializers import  *
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
class ProjectList(generics.ListAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def perform_create(self, serializer):
        serializer.save(lead = self.request.user)

    def get_queryset(self, *args, **kwargs):

        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        return qs.filter(Q(lead = user) | Q(member = user) | Q(assist = user))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request

        return context


class CreateUser(generics.CreateAPIView):

    model = User
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []

class ProjectCreate(generics.CreateAPIView):

    model = Project
    serializer_class = ProjectCreateSerializer

    def perform_create(self, serializer):
        serializer.save(lead = self.request.user)

class ProjectEdit(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    lookup_field = 'token'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
@api_view(['POST'])
def add_member(request, token):

    notfound = []
    added_num = 0
    project = Project.objects.get(token = token)

    usernames = request.data.get("username")

    if type(usernames) == list :
        for username in  usernames:
            try:
                user = User.objects.get(username = username)
            except:
                notfound.append(username)
            else:
                project.member.add(user)
                project.save()
                added_num +=1
    else :
        try:
            user = User.objects.get(username = usernames)
        except:
            notfound.append(usernames)
        else:
                project.member.add(user)
                project.save()
                added_num +=1


    notfound_num = len(notfound)
    return Response(f'{added_num}  Members added successfuly. {notfound_num} usernames not found !  List of unavailable usernames: {notfound}')
@api_view(['POST'])
def add_assist(request, token):

    notfound = []
    added_num = 0
    project = Project.objects.get(token = token)

    usernames = request.data.get("username")

    if type(usernames) == list :
        for username in  usernames:
            try:
                user = User.objects.get(username = username)
            except:
                notfound.append(username)
            else:
                project.assist.add(user)
                project.save()
                added_num +=1
    else :
        try:
            user = User.objects.get(username = usernames)
        except:
            notfound.append(usernames)
        else:
                project.assist.add(user)
                project.save()
                added_num +=1


    notfound_num = len(notfound)
    return Response(f'{added_num}  Assistants added successfuly. {notfound_num} usernames not found !  List of unavailable usernames: {notfound}')
# class Project
# # Create your views here.
