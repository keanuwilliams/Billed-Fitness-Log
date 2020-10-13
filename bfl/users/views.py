from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import (
    update_session_auth_hash,
    authenticate,
    login as dj_login,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    EditWorkoutInfoForm,
    EditUnitsForm,
    EditCategoryForm
)
from .models import Profile


def landing(request):
    if request.user.is_authenticated:
        return redirect('user-home')
    return render(request, 'users/landing.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('user-home')
    else:
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
                        return redirect('user-home')
                else:
                    messages.warning(request, "Invalid username or password.")
            elif not User.objects.get(username=form.data.get('username')).is_active:
                messages.warning(request, "Please contact an admin to reactivate your account.")
            else:
                messages.warning(request, "Invalid username or password.")
        form = AuthenticationForm()
        context = {
            'title': 'Login',
            'form': form,
        }
        return render(request, 'users/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('user-home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_profile = Profile(user=User.objects.get(username=username))
            user_profile.save()
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
        'title': 'Home',
    }
    return render(request, 'users/user-home.html', context)


@login_required
def profile(request, username):
    try:
        user_profile = Profile.objects.get(user=User.objects.get(username=username))
    except User.DoesNotExist:
        raise Http404
    else:
        username = user_profile.user.username
        name = user_profile.user.first_name + ' ' + user_profile.user.last_name
        title = name + ' (@' + username + ')'
        context = {
            'title': title,
            'object': user_profile,
        }
        return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    else:
        if user != request.user:
            messages.warning(request, f'You are not authorized to edit this profile, but you are able to '
                                      f'edit your own.')
            return redirect('edit-profile', request.user.username)
        else:
            if request.method == 'POST':
                username = request.user.username
                user_form = UserUpdateForm(request.POST, instance=request.user)
                profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request, f'Your account has been updated!')
                    referer = request.POST.get('next')
                    if referer:
                        if '/settings/' in referer:
                            return redirect('settings')
                        elif user_form.cleaned_data.get('username'):
                            return redirect('profile', username)
                        else:
                            return redirect('profile', user_form.cleaned_data.get('username'))
                    else:
                        return redirect('profile', user_form.cleaned_data.get('username'))
            else:
                referer = request.META.get('HTTP_REFERER')
                if referer is None:
                    referer = reverse('profile', args=[request.user.username])
                user_form = UserUpdateForm(instance=request.user)
                profile_form = ProfileUpdateForm(instance=request.user.profile)

            context = {
                'title': 'Edit Profile',
                'user_form': user_form,
                'profile_form': profile_form,
                'referer': referer,
            }
            return render(request, 'users/edit-profile.html', context)


@login_required
def settings(request):
    context = {
        'title': 'Settings',
    }
    return render(request, 'users/settings.html', context)


@login_required
def edit_user_preferences(request):
    if request.method == "POST":
        user_form = EditWorkoutInfoForm(request.POST, instance=request.user.profile)
        unit_form = EditUnitsForm(request.POST, instance=request.user.profile)
        cat_form = EditCategoryForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and cat_form.is_valid() and unit_form.is_valid():
            user_form.save()
            unit_form.save()
            cat_form.save()
            messages.success(request, 'Workout information was successfully updated.')
            return redirect('settings')
        else:
            messages.warning(request, 'There was an error updating your profile.')
    else:
        user_form = EditWorkoutInfoForm(instance=request.user.profile)
        unit_form = EditUnitsForm(instance=request.user.profile)
        cat_form = EditCategoryForm(instance=request.user.profile)
    context = {
        'title': 'Edit User Preferences',
        'user_form': user_form,
        'unit_form': unit_form,
        'cat_form': cat_form,
    }
    return render(request, 'users/edit-user-preferences.html', context)


@login_required
def deactivate(request):
    if request.method == "POST":
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, f'{user.username} was successfully deactivated.')
        return redirect('logout')
    context = {
        'title': 'Deactivate',
    }
    return render(request, 'users/deactivate.html', context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password was successfully changed.')
            return redirect('settings')
        else:
            messages.warning(request, 'There was an error changing your password.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'title': 'Change Password',
        'form': form,
    }
    return render(request, 'users/change-password.html', context)
