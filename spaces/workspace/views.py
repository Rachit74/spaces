from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q


from .forms import WorkspaceCreationForm
from .models import Workspace, WorkspaceRequest
from .decorators import user_membership_check


def index(request):
    return redirect('home')

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_workspaces = Workspace.objects.filter(Q(creator=request.user) | Q(members=request.user))
    else:
        user_workspaces = []  # Empty list for unauthenticated users

    context = {
        'user_workspaces': user_workspaces,
    }
    return render(request, 'workspace/index.html', context=context)

@login_required
def create_workspace(request):
    if request.method == 'POST':
        form = WorkspaceCreationForm(request.POST, user=request.user)  # Pass user explicitly
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.creator = request.user  # Assign creator if applicable
            workspace.save()

            # Save many-to-many relationships
            form.save_m2m()

            return redirect('home')  # Redirect to workspace home
    else:
        form = WorkspaceCreationForm(user=request.user)  # Pass user explicitly

    context = {
        'form': form
    }
    return render(request, 'workspace/create.html', context=context)

@login_required
@user_membership_check
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

@login_required
@user_membership_check
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

# search workspace view
def search_workspace(request):
    query = request.GET.get('query', '').strip()
    workspaces = None

    if query:
        workspaces = Workspace.objects.filter(name__icontains=query)

    context = {
        'workspaces': workspaces,
        'user': request.user,
        'query': query,
    }

    return render(request, 'workspace/search_workspace.html', context=context)


# Send reuqest view
"""
create a new WorkspaceRequest entry
"""
def send_workspace_request(request, workspace_id):
    user = request.user
    workspace = get_object_or_404(Workspace, id=workspace_id)

    workspace_request = WorkspaceRequest(user=user, workspace=workspace)
    workspace_request.save()

    messages.success(request, 'Your request was sent!')
    return redirect('search-workspace')
    

# workspace request page
@login_required
@user_membership_check
def joining_requests(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    joining_requests = WorkspaceRequest.objects.filter(workspace=workspace)

    context = {
        'joining_requests': joining_requests,
        'workspace_id': workspace_id,
    }

    return render(request, 'workspace/joining_requests.html', context=context)


# Workspace request approve
def approve_join(request, workspace_id, request_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    request_ = get_object_or_404(WorkspaceRequest, id=request_id)

    workspace.members.add(request_.user)
    workspace.save()

    request_.delete()

    messages.success(request, f"{request_.user} is now a member of your workspace")
    return redirect('joining-requests', workspace_id=workspace_id)
    
# Workspace request approve
def reject_join(request, workspace_id, request_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    request_ = get_object_or_404(WorkspaceRequest, id=request_id)

    workspace.members.remove(request_.user)
    workspace.save()

    request_.delete()
    messages.warning(request, f"{request_.user} was rejected to join the workspace")
    return redirect('joining-requests', workspace_id=workspace_id)