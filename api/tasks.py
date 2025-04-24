import time

from  django.core.mail import send_mail
from celery import shared_task
@shared_task
def send_welcome_email(username,email,token):
    subject = 'Welcome!'
    message = f'Hello {username}  \n This is your token number for api authentication : {token}\nFor send request add header Authorization : {token}'
    recipient_list = [email]
    send_mail(subject, message, 'mohamadrezabjr@gmail.com', recipient_list, fail_silently=False)

@shared_task
def send_task_create_email(lead, recipient_list, project_name,as_who, url):
    subject = 'You invited to a project! '
    message = f'The user {lead.username} invited you to the ({project_name}) project as  {as_who}. \n You can see the project in this link : {url}'
    time.sleep(2)
    send_mail(subject, message, 'moahamadrezabjr@gmail.com', recipient_list, fail_silently=False)