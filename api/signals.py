from django.contrib.auth.signals import user_logged_in , user_logged_out
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from core.models import Project
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.cache import cache
@receiver(post_save, sender = User)
def create_auth_token(sender, instance = None,created= False,**kwargs):
    if created:

        token = Token.objects.create(user=instance)
        token.save()

@receiver([user_logged_in,user_logged_out])
@receiver([post_save,post_delete] ,sender = Project)
def delete_cache(sender, **kwargs):
    redis_client = cache._cache.get_client(write=True)
    for key in redis_client.scan_iter("*project_list*"):
        redis_client.delete(key)

