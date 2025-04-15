from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from core.models import *
from .serializers import *
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAssistPermission, IsLeadPermission, IsMemberPermission
from django.core.mail import send_mail
from django.conf import settings
class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def perform_create(self, serializer):
        serializer.save(lead=self.request.user)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        return qs.filter(Q(lead=user) | Q(member=user) | Q(assist=user)).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request

        return context

class ProjectDetail(generics.RetrieveAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    lookup_field = 'token'
    permission_classes = [IsAuthenticated, IsLeadPermission | IsAssistPermission | IsMemberPermission]

class CreateUser(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


class ProjectCreate(generics.CreateAPIView):
    model = Project
    serializer_class = ProjectCreateSerializer
    def perform_create(self, serializer):
        serializer.save(lead=self.request.user)


class ProjectEdit(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated, IsLeadPermission]
    lookup_field = 'token'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


@api_view(['POST'])
def add_member(request, token):

    try :
        project = Project.objects.get(token=token)
    except :
        return Response ({'error' : 'Project not found!'}, status = status.HTTP_404_NOT_FOUND)
    if project.lead != request.user :
        return Response({'error' : "You don't have permission to add members."}, status = status.HTTP_400_BAD_REQUEST)

    not_found = []
    added_num = 0
    usernames = request.data.get("username")

    if type(usernames) != list:

        usernames = [usernames]

    for username in usernames:
        try:
            user = User.objects.get(username=username)
        except:
            not_found.append(username)
        else:
            project.member.add(user)
            project.save()
            added_num += 1



    notfound_num = len(not_found)
    return Response({'message' : f'{added_num} members added successfully.',
                     'not_found_count' : len(not_found),
                     'not_found_usernames' : not_found}, status = status.HTTP_200_OK)

@api_view(['POST'])
def add_assist(request, token):

    try :
        project = Project.objects.get(token=token)
    except :
        return Response ({'error' : 'Project not found!'}, status = status.HTTP_404_NOT_FOUND)

    if project.lead != request.user :
        return Response({'error' : "You don't have permission to add assistants."}, status = status.HTTP_400_BAD_REQUEST)

    not_found = []
    added_num = 0
    usernames = request.data.get("username")

    if type(usernames) != list:
        usernames = [usernames]
    for username in usernames:
        try:
            user = User.objects.get(username=username)
        except:
            not_found.append(username)
        else:
            project.assist.add(user)
            project.save()
            added_num += 1
    subject = 'hello'
    message = 'this is a test'
    recipient_list = ['bjr.mohamadreza@gmail.com']
    send_mail(subject, message, 'moahamadrezabjr@gmail.com', recipient_list, fail_silently=True)

    return Response({'message' : f'{added_num} Assistants added successfully.',
                     'not_found_count' : len(not_found),
                     'not_found_usernames' : not_found}, status = status.HTTP_200_OK)

class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsAssistPermission | IsLeadPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_token'] = self.kwargs.get('token')

        return context

    def perform_create(self, serializer):
        project_token = self.kwargs.get('token')
        project = get_object_or_404(Project, token = project_token)
        serializer.save(project = project)



