from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Workspace

"""
user_membership_check decorator to check if a user is member of the workspace he is trying to access
"""
def user_membership_check(function):
    wraps(function)
    def wrap(request, *args, **kwargs):
        workspace_id = kwargs.get('workspace_id')
        workspace = get_object_or_404(Workspace, id=workspace_id)
        user = request.user

        if user == workspace.creator or user in workspace.members.all():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You can not view this workspace")
    return wrap