from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name = 'project_list'),
    path ('auth/', obtain_auth_token),
    path ('register/', views.CreateUser.as_view()),
    path ('projects/<str:token>/edit', views.ProjectEdit.as_view(),name = 'project_edit'),
    path ('projects/<str:token>', views.ProjectDetail.as_view(),name = 'project_detail'),

    path ('projects/create/', views.ProjectCreate.as_view()),
    path ('projects/<str:token>/add_member/', views.add_member),
    path ('projects/<str:token>/create_task/', views.TaskCreate.as_view(), name = 'task_create'),
    path ('projects/<str:token>/add_assist/', views.add_assist)


]