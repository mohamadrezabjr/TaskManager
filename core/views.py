from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Project, Task
from django.contrib.auth.models import User
def index(request):

    return render(request,'index.html' )

def signup(request):

    if request.method=='POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']



        if User.objects.filter(username = username).exists():
            messages.error(request,"این نام کاربری قبلا انتخاب شده.")
        elif User.objects.filter(email = email).exists():
            messages.error(request, 'این ایمیل قبلا انتخاب شده')
        elif password1 != password2 :
            messages.error(request, 'رمز های عبور با هم مطابقت ندارند')

        else:

            user = User.objects.create(username= username, email = email)
            user.set_password(password1)
            user.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            log = authenticate(username= username, password = password1)
            login(request,log)
            return redirect('index')
    return render(request, 'auth/signup.html')

def signin(request):


    if request.method == 'POST':

        username= request.POST['username']
        password= request.POST['password']

        user= authenticate(username = username, password = password)
        login(request, user)
        return redirect('index')

    return render(request, 'auth/signin.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signin')
    return redirect('index')


def test(request):
    return render(request, 'test.html')

def project_list(request):

    if  not request.user.is_authenticated:
        return redirect('signin')
    user = request.user

    projects = Project.objects.filter(Q(lead = user) | Q(assist=user) | Q(member = user))

    context = {'projects': projects}

    return render(request, 'project_list.html', context)

def project_view(request, token):

    if request.method == 'POST':
        task_title = request.POST['task_title']
        task_description = request.POST['task_description']
        user = User.objects.filter(username = request.POST['user']).first()
        task_project= Project.objects.get(token=token)
        task = Task.objects.create(name = task_title, description=task_description, user= user, project= task_project )
        task.save()
        return redirect('detail', token)
    project = Project.objects.get(token=token)
    members = project.member.all()
    assistants = project.assist.all()
    tasks = Task.objects.filter(project=project)
    context = {'project':project, 'members':members, 'assistants':assistants, 'tasks':tasks}
    return render(request, 'project_detail.html', context=context)









# Create your views here.
