from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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

            user = User.objects.create(username= username, email = email, password = password1)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            log = authenticate(username= username, password = password1)
            login(request,log)
            return redirect('index')
    return render(request, 'auth/signup.html')

def signin(request):


    if request.method == 'POST':

        username= request.POST.get('username')
        password= request.POST.get('password')

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









# Create your views here.
