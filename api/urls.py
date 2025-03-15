from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name = 'project_list'),
    path ('auth/', obtain_auth_token),
    path ('register/', views.CreateUser.as_view()),
    path ('projects/<str:token>/', views.ProjectEdit.as_view()),
    path ('projects/create/', views.ProjectCreate.as_view()),
    path ('projects/<str:token>/add_member/', views.add_member),
    path ('projects/<str:token>/add_assist/', views.add_assist)


]