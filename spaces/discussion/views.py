from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages

# imports from external apps
from workspace.models import Workspace

# imports from self app
from .models import Post, Comment
from .forms import PostCreationForm, CommentCreationForm

# Create your views here.

"""
view for workspace discussion home page
all the topics for dicussion will show up in a list on this page
"""
def workspace_discussion(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    posts = Post.objects.filter(workspace=workspace)

    context = {
        'workspace': workspace,
        'posts': posts,
    }

    return render(request, 'discussion/discuss.html', context=context)

"""
view for topic creation form
"""
def discussion_topic_form(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    if request.method == "POST":
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.workspace = workspace
            post.author = request.user
            post.save()

            messages.success(request, "New topic created!")
            return redirect('workspace-discussion-index', workspace_id=workspace_id)

    else:
        form = PostCreationForm()
        context = {
            'workspace': workspace,
            'form': form
        }

        return render(request, 'discussion/topic_form.html', context=context)
    
"""
particular post view
"""
def topic_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment Added!")
            return redirect('topic-post', post_id=post_id)
    else:
        form = CommentCreationForm()
        comments = Comment.objects.filter(post=post)

    context = {
        'form': form,
        'post': post,
        'comments': comments,
    }

    return render(request, 'discussion/post.html', context=context)

# Delete Topic Post
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user == post.author:
        return HttpResponseForbidden("Forbidden")
    else:
        post.delete()
        return redirect('workspace-discussion-index', workspace_id=post.workspace.id)

# Delete comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user == comment.author:
        return HttpResponseForbidden("Forbidden")
    else:
        comment.delete()
        messages.warning(request, "Comment Delete!")
        return redirect('topic-post', post_id=comment.post.id)