from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def home(request):
    return HttpResponse("Hi")

def user_register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
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
                return redirect('profile')
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
    context = {
        'user': user,
    }
    if user is not None:
        return render(request, 'user/profile.html', context=context)
    else:
        return redirect('login')