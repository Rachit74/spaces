from django.db import models
from django.contrib.auth.models import User

from workspace.models import Workspace


# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    complected = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
