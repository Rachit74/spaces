from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace_home, name='workspace_home'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
]