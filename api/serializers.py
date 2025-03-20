from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import *
from taskmanager.serializers import *
from rest_framework.reverse import reverse
class ProjectListSerializer(serializers.ModelSerializer):

    lead = serializers.SerializerMethodField()
    assist = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse ('project_detail', kwargs = {'token' : obj.token} , request= request)

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
            'url'
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

    member = UserNameSerializer(many = True)
    assist = UserNameSerializer(many = True)

    def create(self, validated_data):

        assists = validated_data.pop('assist')
        members = validated_data.pop('member')
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
