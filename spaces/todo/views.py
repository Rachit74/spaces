from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Todo
from .forms import TodoCreationForm

from workspace.models import Workspace

# Create your views here.
@login_required
def workspace_todo(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    todos = Todo.objects.filter(workspace=workspace)

    context = {
        'todos': todos,
        'workspace': workspace,
    }

    return render(request, 'todo/todo.html', context=context)

@login_required
def todo_creation(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if request.method == "POST":
        form = TodoCreationForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.workspace = workspace
            todo.creator = request.user
            todo.save()

            messages.success(request, "New Todo has been created!")
            return redirect('workspace-todo', workspace_id=workspace.id)
    else:
        form = TodoCreationForm()

    context = {
        'form': form,
        'workspace': workspace,
    }

    return render(request, 'todo/todo_form.html', context)