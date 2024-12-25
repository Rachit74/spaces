from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm
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
