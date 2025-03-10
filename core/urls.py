from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name = 'index'),
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('logout/', views.logout_view, name = 'logout'),
    path('test/', views.test, name = 'test')
]