from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name = 'index'),
    path('signup/', views.signup, name = 'signup'),
    # path('signin/', views.signin, name = 'signin'),
    path('logout/', views.logout_view, name = 'logout'),
    path('test/', views.test, name = 'test'),
    path('projects/', views.project_list, name= 'projects'),
    path('projects/<str:token>/' , views.project_view, name='detail')
]