from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import *
from taskmanager.serializers import *
from rest_framework.reverse import reverse


class UrlSerializer(serializers.Serializer):

    edit_url =  serializers.SerializerMethodField(read_only=True)
    add_member = serializers.SerializerMethodField(read_only=True)
    add_assist = serializers.SerializerMethodField(read_only=True)
    create_task = serializers.SerializerMethodField(read_only=True)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        return reverse('project_edit', kwargs = {'token' : obj.token}, request =request)
    def get_add_member(self, obj):
        request = self.context.get('request')
        return reverse('add_member', kwargs = {'token' : obj.token}, request =request)
    def get_add_assist(self, obj):
        request = self.context.get('request')
        return reverse('add_assist', kwargs = {'token' : obj.token}, request =request)
    def get_create_task(self, obj):
        request = self.context.get('request')
        return reverse('task_create', kwargs = {'token' : obj.token}, request =request)



class ProjectListSerializer(serializers.ModelSerializer):

    lead = serializers.SerializerMethodField()
    assist = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField(read_only=True)

    def get_urls(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        return UrlSerializer(obj, context = context).data
    def get_assist(self, obj):
        context = {'request' : self.context.get('request'),'project':obj}
        return UserPublicSerializer(obj.assist.all(),many = True, context=context).data

    def get_member(self, obj):
        context = {'request' : self.context.get('request'),'project':obj}
        return UserPublicSerializer(obj.member.all(),many = True, context=context).data

    def get_lead(self, obj):
        context = {'request' : self.context.get('request'), 'project':obj}
        return UserPublicSerializer(obj.lead, context=context).data

    class Meta:

        model = Project
        fields = [
            'name',
            'start',
            'deadline',
            'description',
            'lead',
            'assist',
            'member',
            'urls'
        ]

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    def create(self, validated_data):

        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields =  [
            'username',
            'email',
            'password'
        ]

class UserNameSerializer(serializers.Serializer):

    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username'
        ]
class ProjectCreateSerializer(serializers.ModelSerializer):

    member = UserNameSerializer(many = True, required = False)
    assist = UserNameSerializer(many = True, required = False)

    def create(self, validated_data):
        try:
            assists = validated_data.pop('assist')
        except KeyError:
            assists = []
        try :
            members = validated_data.pop('member')
        except KeyError :
            members = []
        project = Project.objects.create(**validated_data)

        for user in assists:
            assist_user= User.objects.get(**user)
            project.assist.add(assist_user)

        for user in members:
            member_user= User.objects.get(**user)
            project.member.add(member_user)

        project.save()
        return project

    class Meta:

        model= Project
        fields = [
            'name',
            'description',
            'assist',
            'member',
            'start',
            'deadline'
        ]
class TaskSerializer(serializers.ModelSerializer):

    project = serializers.CharField(read_only=True)
    username = serializers.CharField(source = 'user')
    class Meta:
        model = Task
        fields = ['username',
                  'project',
                  'name',
                  'description'
        ]



    def create(self, validated_data):
        print(validated_data)

        project_token = self.context.get('project_token')
        project = get_object_or_404(Project, token = project_token)

        username = validated_data.pop('user')
        user = get_object_or_404(User, username = username)
        if project.member.filter(username = username).exists() or project.assist.filter(username = username).exists() :

            task = Task.objects.create(**validated_data, user= user)
            task.save()
            return task
        else :
            raise serializers.ValidationError({'error' : 'This user is not a member or an assistant of this project.'})
