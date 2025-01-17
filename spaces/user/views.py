from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout

from workspace.models import Workspace
from .models import Profile
from django.contrib.auth.models import User

from django.db.models import Q

# Create your views here.
def home(request):
    return HttpResponse("Hi")

def user_register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request, user)
            return redirect('workspace')
    else:
        form = UserRegistrationForm
    
    context = {
        'form': form,
    }

    return render(request, 'user/register.html', context=context)

def user_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # .get('username') form cleaned_data dict
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("User Logged in")
                return redirect('home')
    else:
        form = UserLoginForm

    context = {
        'form': form,
    }

    return render(request, 'user/login.html', context=context)

def user_logout_view(request):
    logout(request)
    return redirect('login')

def user_profile_view(request):
    user = request.user
    user_spaces = Workspace.objects.filter(creator=user)
    spaces_member = Workspace.objects.filter(Q(members=user))
    context = {
        'user': user,
        'user_spaces': user_spaces,
        'spaces_member': spaces_member,
    }
    if user is not None:
        return render(request, 'user/profile.html', context=context)
    else:
        return redirect('login')
    
def user_search(request):
    query = request.GET.get('query', '').strip()
    users = None

    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    context = {
        'users': users,
        'query': query,
        'current_user': request.user
    }

    return render(request, 'user/search_page.html',context=context)

def delete_account_view(request):
    user = request.user
    User.objects.delete(id=user.id)

    print("User deleted")
    return redirect('login')

# add user view
def add_user(request, user_id):
    user = request.user #current user
    user_added = get_object_or_404(User, id=user_id)

    user.profile.follows.add(user_added.profile)

    return redirect('search')

# remove user view
def remove_user(request, user_id):
    user = request.user
    user_removed = get_object_or_404(User, id=user_id)

    user.profile.follows.remove(user_removed.profile)
    
    return redirect('search')