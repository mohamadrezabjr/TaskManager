import time
from django.conf import settings
from  django.core.mail import send_mail
from celery import shared_task
from django.contrib.auth.models import User

@shared_task
def send_welcome_email(username,email,token):
    subject = 'Welcome!'
    message = f'Hello {username}  \n This is your token number for api authentication : {token}\nFor send request add header Authorization : {token}'
    recipient_list = [email]
    send_mail(subject, message, 'mohamadrezabjr@gmail.com', recipient_list, fail_silently=False)

@shared_task
def send_task_create_email(lead, recipient_list, project_name,as_who, url="/"):
    subject = 'You invited to a project! '
    message = f'The user {lead} invited you to the ({project_name}) project as  {as_who}.'
    if url != '/':
        message = message + f' \n You can see the project in this link : {url}'

    send_mail(subject, message, from_email = settings.EMAIL_HOST_USER, recipient_list= recipient_list, fail_silently=False)

@shared_task
def one_day(project_name ,deadline, receivers):
    subject = "Final Reminder: 1 Day Left Until Project Deadline"

    for receiver in receivers:
        user = User.objects.get(username =receiver)
        email = user.email
        recipient_list = [email]

        message = f"""
        Dear {receiver},\n\n

        I hope this message finds you well.\n

        This is a kind reminder that there is only one day remaining until the deadline for the {project_name}. The final due date is {deadline}, and we kindly ask that all remaining work be completed and submitted by then.

        """
        send_mail(subject=subject, message=message, from_email = settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
