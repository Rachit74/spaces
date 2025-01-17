from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from django.db.models import Q


from .forms import WorkspaceCreationForm, PostCreationForm, CommentCreationForm
from .models import Workspace, Post, Comment

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
    

def workspace_discussion(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    posts = Post.objects.filter(workspace=workspace)

    context = {
        'workspace': workspace,
        'posts': posts,
    }

    return render(request, 'workspace/discuss.html', context=context)


def discussion_topic_form(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    if request.method == "POST":
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.workspace = workspace
            post.author = request.user
            post.save()
            return redirect('workspace_discussion', workspace_id=workspace_id)

    else:
        form = PostCreationForm()
        context = {
            'workspace': workspace,
            'form': form
        }

        return render(request, 'workspace/topic_form.html', context=context)
    
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post', post_id=post_id)
    else:
        form = CommentCreationForm()
        comments = Comment.objects.filter(post=post)

    context = {
        'form': form,
        'post': post,
        'comments': comments,
    }

    return render(request, 'workspace/post.html', context=context)

# Delete comment view
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user == comment.author:
        return HttpResponseForbidden("Forbidden")
    else:
        comment.delete()
        return redirect('post', post_id=comment.post.id)
    
# Delete post view
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user == post.author:
        return HttpResponseForbidden("Forbidden")
    else:
        post.delete()
        return redirect('workspace_discussion', workspace_id=post.workspace.id)

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