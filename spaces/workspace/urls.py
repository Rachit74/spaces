from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace_home, name='workspace_home'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
    path('delete_workspace/<int:workspace_id>', views.delete_workspace, name='delete_workspace'),
    path('workspace/<int:workspace_id>', views.workspace_view, name='workspace_view'),
    path('workspace/<int:workspace_id>/discuss', views.workspace_discussion, name='workspace_discussion'),
]