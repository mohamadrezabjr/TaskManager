from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('', views.ProjectList.as_view(), name = 'project_list_create'),
    path ('auth/', obtain_auth_token),
    path ('register/', views.CreateUser.as_view())

]