from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Workout
from .forms import WorkoutForm


@login_required
def my_workouts(request):
    workouts = Workout.objects.filter(user=request.user)

    context = {
        'title': 'My Workouts',
        'all': False,
        'workouts': workouts.order_by('-date')
    }
    return render(request, 'log/workout-list.html', context)


@login_required
def all_workouts_admin(request):
    if not request.user.is_superuser:
        redirect('my-workouts')
    workouts = Workout.objects.all()

    context = {
        'title': 'All Workouts',
        'all': True,
        'workouts': workouts.order_by('-date')
    }
    return render(request, 'log/workout-list.html', context)


@login_required
def workout_detail(request, pk):
    try:
        workout = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        raise Http404
    else:
        if request.user != workout.user and not request.user.is_superuser:
            messages.warning(request, f'You do not have access to this workout.')
            return redirect('my-workouts')
        else:
            title = workout.name
            if request.META.get('HTTP_REFERER'):
                if '/new/' in request.META.get('HTTP_REFERER') \
                        or '/edit/' in request.META.get('HTTP_REFERER') \
                        or '/delete/' in request.META.get('HTTP_REFERER'):
                    if request.user.is_superuser and '/all/' in request.META.get('HTTP_REFERER'):
                        referer = reverse('all-workouts-admin')
                    else:
                        referer = reverse('my-workouts')
                else:
                    referer = request.META.get('HTTP_REFERER')
            else:
                referer = reverse('my-workouts')

            context = {
                'title': title,
                'workout': workout,
                'referer': referer,
            }
            return render(request, 'log/workout-detail.html', context)


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = 'log/workout-form.html'
    form_class = WorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Workout'
        context['page_title'] = 'New Workout'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    template_name = 'log/workout-form.html'
    form_class = WorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit ' + self.object.name
        context['page_title'] = self.object.name
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user or self.request.user.is_superuser:
            return True
        return False


class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    success_url = '/workouts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete ' + self.object.name
        return context

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user or self.request.user.is_superuser:
            return True
        return False

