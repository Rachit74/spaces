from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workspaces')
    members = models.ManyToManyField(User, related_name='workspaces')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


"""
Post and Comment Models for discussion in workspaces
"""

class Post(models.Model):
    # each post is under a specific workspace
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=False, null=False)
    # posts can't be deleted if a user gets deleted, posts can be usefull in future possibly.
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # auto_now_add only sets when the record is created and does not change afterwards
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now is changed whenever the recored is updated and saved again
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
