from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from .forms import WorkspaceCreationForm
from .models import Workspace

# Create your views here.
def workspace_home(request):
    if request.user.is_authenticated:
        user_workspaces = Workspace.objects.filter(creator=request.user)
    else:
        user_workspaces = []  # Empty list for unauthenticated users

    context = {
        'user_workspaces': user_workspaces,
    }
    return render(request, 'workspace/index.html', context=context)


def create_workspace(request):
    if request.method == 'POST':
        form = WorkspaceCreationForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.creator = request.user
            workspace.save()

            # many to many field needs extra care
            form.save_m2m()

            return redirect('workspace_home')
    else:
        form = WorkspaceCreationForm

    context = {
        'form': form
    }
    return render(request, 'workspace/create.html', context=context)

def delete_workspace(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    user = request.user

    if workspace.creator != user:
        pass
    else:
        workspace.delete()

    return redirect('profile')