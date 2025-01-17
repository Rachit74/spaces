from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace_home, name='workspace_home'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
    path('delete_workspace/<int:workspace_id>', views.delete_workspace, name='delete_workspace'),
    path('workspace/<int:workspace_id>', views.workspace_view, name='workspace_view'),

    path('search_workspaces/', views.search_workspace, name='search_workspace'),
    path('send_workspace_request/<int:workspace_id>', views.send_workspace_request, name='send_workspace_request'),

    path('workspace/<int:workspace_id>/requests', views.joining_requests, name='joining_requests'),

    path('workspace/<int:workspace_id>/approve_join/<int:request_id>', views.approve_join, name='approve_join'),
    path('workspace/<int:workspace_id>/reject_join/<int:request_id>', views.reject_join, name='reject_join'),
]