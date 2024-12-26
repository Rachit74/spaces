from django.shortcuts import render, HttpResponse, redirect

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

            return redirect('workspace_home')
    else:
        form = WorkspaceCreationForm

    context = {
        'form': form
    }
    return render(request, 'workspace/create.html', context=context)