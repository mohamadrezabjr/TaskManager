from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):

    name = models.CharField(max_length=255)
    lead = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    assist = models.ManyToManyField(User, blank = True, related_name='assist')
    member = models.ManyToManyField(User, blank = True, related_name='member')
    created = models.DateTimeField(auto_now_add=True)

class Task(models.Model):

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
# Create your models here.
