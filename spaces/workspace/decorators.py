from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Workspace
from discussion.models import Post

"""
user_membership_check decorator to check if a user is member of the workspace he is trying to access
"""
def user_membership_check(function):
    wraps(function)
    def wrap(request, *args, **kwargs):
        workspace_id = kwargs.get('workspace_id')

        # check if workspace id is none (for post discussion page)
        if workspace_id == None:
            post_id = kwargs.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            workspace_creator = post.workspace.creator
            workspace_members = post.workspace.members.all()
        else:        
            workspace = get_object_or_404(Workspace, id=workspace_id)
            workspace_creator = workspace.creator
            workspace_members = workspace.members.all()
        
        user = request.user

        if user == workspace_creator or user in workspace_members:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You can not view this workspace")
    return wrap