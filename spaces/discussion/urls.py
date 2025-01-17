from django.urls import path

from . import views

urlpatterns = [

    path('<int:workspace_id>/', views.workspace_discussion, name='workspace-discussion-index'),
    path('<int:workspace_id>/create_topic/', views.discussion_topic_form, name='discussion-topic-form'),
    path('post/<int:post_id>/', views.topic_post, name='topic-post'),

    path('delete/post/<int:post_id>', views.delete_post, name='delete-post'),
    path('delete/comment/<int:comment_id>', views.delete_comment, name='delete-comment'),
]