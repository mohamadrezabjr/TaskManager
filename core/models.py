from django.db import models
from django.contrib.auth.models import User
import string , random
def make_token(type, length):
    token = ''.join(random.choices(string.digits, k= length))
    return f'{type}-{token}'

class Project(models.Model):

    name = models.CharField(max_length=255)
    lead = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    assist = models.ManyToManyField(User, blank = True, related_name='assist')
    member = models.ManyToManyField(User, blank = True, related_name='member')
    description = models.TextField(blank = True, null = True)
    token = models.CharField(max_length=11, blank=True, null = True)
    start = models.DateField()
    deadline = models.DateField()

    def save(self, *args, **kwargs):

        if not self.token:
            self.token= make_token('P',9)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} token : {self.token}'
class Task(models.Model ):

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE,related_name='tasks')

    def __str__(self):
        return f'{self.user}\'s task for Project : {self.project.name}'
# Create your models here.
