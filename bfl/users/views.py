from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def landing(request):
    return render(request, 'users/landing.html')

def login(request):
    context = {
        'title': 'Login'
    }
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}!')
            return redirect('landing')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'users/register.html', context)
