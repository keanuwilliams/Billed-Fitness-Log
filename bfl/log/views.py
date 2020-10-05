from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Workout
from .forms import WorkoutForm


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Workouts'
        context['all'] = False
        return context

    def get_queryset(self):
        queryset = Workout.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


class WorkoutAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Workout
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Workouts'
        context['all'] = True
        return context

    def get_queryset(self):
        queryset = Workout.objects.all()
        return queryset.order_by(self.ordering)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class WorkoutDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        if self.request.META.get('HTTP_REFERER'):
            if '/new/' in self.request.META.get('HTTP_REFERER') \
                    or '/edit/' in self.request.META.get('HTTP_REFERER') \
                    or '/delete/' in self.request.META.get('HTTP_REFERER'):
                if self.request.user.is_superuser and '/all/' in self.request.META.get('HTTP_REFERER'):
                    context['referer'] = reverse('workout-admin-list')
                else:
                    context['referer'] = reverse('workout-list')
            else:
                context['referer'] = self.request.META.get('HTTP_REFERER')
        else:
            context['referer'] = reverse('workout-list')
        return context

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user or self.request.user.is_superuser:
            return True
        return False


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
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

