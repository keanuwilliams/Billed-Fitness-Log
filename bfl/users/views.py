from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as dj_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def landing(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    return render(request, 'users/landing.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    else:
        logout(request)
        username = ''
        password = ''
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        dj_login(request, user)
                        messages.success(request, "Login successful!")
                        return redirect('user_home')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        context = {
            'title': 'Login',
            'form': form,
        }
        return render(request, 'users/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            profile = Profile(user=User.objects.get(username=username))
            profile.save()
            messages.success(request, f'Account successfully created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'users/register.html', context)

@login_required
def user_home(request):
    context = {
        'title': 'User Home',
    }
    return render(request, 'users/user-home.html', context)

@login_required
def profile(request):
    username = request.user.username
    name = request.user.first_name + ' ' + request.user.last_name
    title = name + ' (@' + username + ')'
    context = {
        'title': title,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Edit Profile',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/edit-profile.html', context)
