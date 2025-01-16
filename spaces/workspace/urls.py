from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace_home, name='workspace_home'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
    path('delete_workspace/<int:workspace_id>', views.delete_workspace, name='delete_workspace'),
    path('workspace/<int:workspace_id>', views.workspace_view, name='workspace_view'),
    path('workspace/<int:workspace_id>/discuss', views.workspace_discussion, name='workspace_discussion'),
    path('workspace/<int:workspace_id>/topic_form', views.discussion_topic_form, name='topic_form'),
    path('post/<int:post_id>', views.post_view, name='post'),

    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
]