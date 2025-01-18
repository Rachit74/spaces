from django.urls import path

from . import views

urlpatterns = [
    path('<int:workspace_id>/', views.workspace_todo, name='workspace-todo'),
    path('<int:workspace_id>/create', views.todo_creation, name='todo-creation-form'),
]