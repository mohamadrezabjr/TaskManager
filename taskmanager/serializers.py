from rest_framework import serializers
from core.models import *
class TaskPublicSerializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)



class UserPublicSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.CharField(read_only=True)
    # user_tasks = serializers.SerializerMethodField(read_only=True)
    #
    # def get_user_tasks(self, obj):
    #     user = obj
    #
    #     qs = Task.objects.filter(user = user)
    #     return TaskPublicSerializer(qs , many=True, read_only=True)