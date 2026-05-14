from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:id>/', views.project_board, name='project_board'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:id>/status/', views.task_update_status, name='task_update_status'),
    path('tasks/<int:id>/delete/', views.task_delete, name='task_delete'),
    path('team/', views.team_list, name='team_list'),
    path('team/<int:id>/role/', views.team_update_role, name='team_update_role'),
    path('team/<int:id>/delete/', views.team_delete, name='team_delete'),
]
