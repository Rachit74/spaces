from django.shortcuts import render, HttpResponse

# Create your views here.
def workspace_home(request):
    return render(request, 'workspace/index.html')