from rest_framework import serializers
from core.models import *
from taskmanager.serializers import *
class ProjectListSerializer(serializers.ModelSerializer):

    lead = UserPublicSerializer(read_only=True)
    assist = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_assist(self, obj):
        return UserPublicSerializer(obj.assist.all(),many = True, context={'project':obj}).data


    def get_member(self, obj):
        return UserPublicSerializer(obj.member.all(),many = True, context={'project':obj}).data

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

        model = Project
        fields = [
            'name',
            'description',
            'lead',
            'assist',
            'member',
            'start',
            'deadline'
        ]


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    def create(self, validated_data):

        password = validated_data.pop('password')
        print(password)
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



