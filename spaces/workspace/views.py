from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from django.db.models import Q


from .forms import WorkspaceCreationForm
from .models import Workspace

# Create your views here.
def workspace_home(request):
    if request.user.is_authenticated:
        user_workspaces = Workspace.objects.filter(Q(creator=request.user) | Q(members=request.user))
    else:
        user_workspaces = []  # Empty list for unauthenticated users

    context = {
        'user_workspaces': user_workspaces,
    }
    return render(request, 'workspace/index.html', context=context)


def create_workspace(request):
    if request.method == 'POST':
        form = WorkspaceCreationForm(request.POST, user=request.user)  # Pass user explicitly
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.creator = request.user  # Assign creator if applicable
            workspace.save()

            # Save many-to-many relationships
            form.save_m2m()

            return redirect('workspace_home')  # Redirect to workspace home
    else:
        form = WorkspaceCreationForm(user=request.user)  # Pass user explicitly

    context = {
        'form': form
    }
    return render(request, 'workspace/create.html', context=context)


def delete_workspace(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    user = request.user

    # if the creator of the workspace is not the user deleting it, forbid the action
    if workspace.creator != user:
        return HttpResponseForbidden("You can not perform this action as you are not the creator of the workspace")
    else:
        # allow otherwise
        workspace.delete()

    return redirect('profile')

def workspace_view(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    user = request.user

    # Allow the creator and members of the workspace to visit the workspace
    if user in workspace.members.all() or workspace.creator == user:
        context = {
            'workspace': workspace,
        }
        return render(request, 'workspace/workspace.html', context=context)
    else:
        # Forbid outsiders to visit the workspace
        return HttpResponseForbidden("You are not authorized to view this workspace.")
