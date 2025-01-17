from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_workspace, name='create-workspace'),
    path('delete/<int:workspace_id>', views.delete_workspace, name='delete-workspace'),
    path('<int:workspace_id>', views.workspace_view, name='workspace'),

    path('search/', views.search_workspace, name='search-workspace'),
    path('send_request/<int:workspace_id>', views.send_workspace_request, name='send-workspace-request'),

    path('<int:workspace_id>/requests', views.joining_requests, name='joining-requests'),

    path('<int:workspace_id>/approve_join/<int:request_id>', views.approve_join, name='approve-join'),
    path('<int:workspace_id>/reject_join/<int:request_id>', views.reject_join, name='reject-join'),
]