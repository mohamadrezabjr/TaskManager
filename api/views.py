import time

from django.dispatch import receiver

from .tasks import send_task_create_email,  one_day

from datetime import datetime , timedelta
from django.shortcuts import render, get_object_or_404
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from core.models import *
from core.views import project_list
from .serializers import *
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAssistPermission, IsLeadPermission, IsMemberPermission
from django.core.mail import send_mail
from django.conf import settings

#cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


#api/projects
class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    @method_decorator(cache_page(60*3, key_prefix = project_list))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super(ProjectList, self).list(request, *args, **kwargs)

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
#api/projects/<token>/
class ProjectDetail(generics.RetrieveAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    lookup_field = 'token'
    permission_classes = [IsAuthenticated, IsLeadPermission | IsAssistPermission | IsMemberPermission]

#api/register/
class CreateUser(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

#api/create_project
class ProjectCreate(generics.CreateAPIView):
    model = Project
    serializer_class = ProjectCreateSerializer

    def perform_create(self, serializer):


        serializer.save(lead=self.request.user)

        project_name = serializer.validated_data['name']
        deadline = serializer.validated_data['deadline']
        member = serializer.validated_data.get("member_usernames")
        assist = serializer.validated_data.get("assist_usernames")
        if not assist:
            assist=[]
        if not member:
            member=[]

        receivers = assist+member

        one_day_left = deadline - timedelta(days = 1)

        one_day.apply_async(eta = one_day_left, kwargs = {"project_name": project_name, "deadline": deadline, "receivers" :receivers})


#api/projects/<token>/edit/
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

#api/projects/<token>/add_member/
@api_view(['POST'])
def add_member(request, token):


    try :
        project = Project.objects.get(token=token)
        lead = project.lead
    except :
        return Response ({'error' : 'Project not found!'}, status = status.HTTP_404_NOT_FOUND)
    #just leader can add member
    if project.lead != request.user :
        return Response({'error' : "You don't have permission to add members."}, status = status.HTTP_400_BAD_REQUEST)

    project_members = project.member.all()
    not_found = []
    added_num = 0
    already_member = []
    usernames = request.data.get("username")

    #get one user or a list of users . for example : {"username":"blabla"} or {"username" : ["blabla1","blabla2"]}
    if type(usernames) != list:

        usernames = [usernames]

    recipient_list =[]
    for username in usernames:
        try:
            user = User.objects.get(username=username)
        except:
            not_found.append(username)
        else:
            if user not in project_members :
                project.member.add(user)
                project.save()
                added_num += 1

                recipient_list.append(user.email)
            else :
                already_member.append(username)

    url = reverse('project_detail', kwargs = {'token' : token}, request =request)
    send_task_create_email.delay(lead =lead.username,recipient_list = recipient_list ,project_name = project.name,url =url,as_who = 'member')


    return Response({'message' : f'{added_num} members added successfully.',
                     'not_found_count' : len(not_found),
                     'not_found_usernames' : not_found,
                     'These users are already member in this project : ' : already_member},
                      status = status.HTTP_200_OK)

#api/projects/<token>/add_assist/
@api_view(['POST'])
def add_assist(request, token):

    try :
        project = Project.objects.get(token=token)
        lead = project.lead
    except :
        return Response ({'error' : 'Project not found!'}, status = status.HTTP_404_NOT_FOUND)

    if lead != request.user :
        return Response({'error' : "You don't have permission to add assistants."}, status = status.HTTP_400_BAD_REQUEST)

    project_assists = project.assist.all()
    not_found = []
    added_num = 0
    usernames = request.data.get("username")
    already_assist = []

    # get one user or a list of users . for example : {"username":"blabla"} or {"username" : ["blabla1","blabla2"]}
    if type(usernames) != list:
        usernames = [usernames]
    recipient_list = []

    for username in usernames:
        try:
            user = User.objects.get(username=username)
        except:
            not_found.append(username)
        else:
            if user not in project_assists :

                project.assist.add(user)
                project.save()
                recipient_list.append(user.email)
                added_num += 1
            else :
                already_assist.append(username)

    url = reverse('project_detail', kwargs = {'token' : token}, request =request)

    send_task_create_email.delay(lead =lead.username,recipient_list = recipient_list ,project_name = project.name,url =url,as_who = 'assistant')

    return Response({'message' : f'{added_num} Assistants added successfully.',
                     'not_found_count' : len(not_found),
                     'not_found_usernames' : not_found,
                     'These users are already assist in this project : ' : already_assist},
                     status = status.HTTP_200_OK)

#api/projects/<token>/create_task/
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



