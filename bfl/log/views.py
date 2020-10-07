from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WLWorkout, RWorkout, CWorkout
from .forms import WLWorkoutForm, RWorkoutForm, CWorkoutForm


class CWorkoutListView(ListView, LoginRequiredMixin):
    model = CWorkout
    template_name = 'log/workout-single-list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Cardio Workouts'
        context['category'] = 'CARDIO'
        context['th_1'] = 'Sets'
        context['th_2'] = 'Time'
        context['th_3'] = 'Distance'
        return context

    def get_queryset(self):
        queryset = CWorkout.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


class RWorkoutListView(ListView, LoginRequiredMixin):
    model = WLWorkout
    template_name = 'log/workout-single-list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Resistance Workouts'
        context['category'] = 'RESISTANCE'
        context['th_1'] = 'Resistance'
        context['th_2'] = 'Sets'
        context['th_3'] = 'Reps'
        return context

    def get_queryset(self):
        queryset = RWorkout.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


class WLWorkoutListView(ListView, LoginRequiredMixin):
    model = WLWorkout
    template_name = 'log/workout-single-list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Weightlifting Workouts'
        context['category'] = 'WEIGHTLIFTING'
        context['th_1'] = 'Weight'
        context['th_2'] = 'Sets'
        context['th_3'] = 'Reps'
        return context

    def get_queryset(self):
        queryset = WLWorkout.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


@login_required
def my_workouts(request):
    c_workouts = CWorkout.objects.filter(user=request.user)
    r_workouts = RWorkout.objects.filter(user=request.user)
    wl_workouts = WLWorkout.objects.filter(user=request.user)

    context = {
        'title': 'My Workouts',
        'all': False,
        'c_workouts': c_workouts.order_by('-date')[:3],
        'r_workouts': r_workouts.order_by('-date')[:3],
        'wl_workouts': wl_workouts.order_by('-date')[:3],
    }
    return render(request, 'log/workout-list.html', context)


@login_required
def all_workouts_admin(request):
    if not request.user.is_superuser:
        redirect('my-workouts')
    c_workouts = CWorkout.objects.all()
    r_workouts = RWorkout.objects.all()
    wl_workouts = WLWorkout.objects.all()

    context = {
        'title': 'All Workouts',
        'all': True,
        'c_workouts': c_workouts.order_by('-date')[:10],
        'r_workouts': r_workouts.order_by('-date')[:10],
        'wl_workouts': wl_workouts.order_by('-date')[:10],
    }
    return render(request, 'log/workout-list.html', context)


@login_required
def select_workouts(request):

    context = {
        'title': 'Select Workout Type',
        'page_title': 'Select Workout Type',
    }
    return render(request, 'log/workout-select.html', context)


@login_required
def wl_workout_detail(request, pk):
    try:
        workout = WLWorkout.objects.get(pk=pk)
    except WLWorkout.DoesNotExist:
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

            if workout.user.profile.weight_units == 'P':
                units = 'lbs'
            else:
                units = 'kg'

            context = {
                'title': title,
                'workout': workout,
                'num1_title': 'Sets',
                'num2_title': 'Reps',
                'num3_title': 'Weight',
                'num1_value': workout.sets,
                'num2_value': workout.reps,
                'num3_value': workout.weight,
                'num3_units': units,
                'referer': referer,
                'update': reverse('edit-wl-workout', args=[str(workout.id)]),
                'delete': reverse('delete-wl-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


@login_required
def r_workout_detail(request, pk):
    try:
        workout = RWorkout.objects.get(pk=pk)
    except RWorkout.DoesNotExist:
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

            if workout.resistance == 'E':
                resistance = 'Easy'
            elif workout.resistance == 'M':
                resistance = 'Medium'
            elif workout.resistance == 'D':
                resistance = 'Difficult'
            else:
                resistance = 'Advanced'

            context = {
                'title': title,
                'workout': workout,
                'num1_title': 'Sets',
                'num2_title': 'Reps',
                'num3_title': 'Resistance',
                'num1_value': workout.sets,
                'num2_value': workout.reps,
                'num3_value': resistance,
                'num3_units': '',
                'referer': referer,
                'update': reverse('edit-r-workout', args=[str(workout.id)]),
                'delete': reverse('delete-r-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


@login_required
def c_workout_detail(request, pk):
    try:
        workout = CWorkout.objects.get(pk=pk)
    except CWorkout.DoesNotExist:
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

            distance = workout.distance
            if workout.user.profile.distance_units == 'M':
                units = 'miles'
            else:
                units = 'kilometers'

            hour = str(workout.time.hour)
            minute = str(workout.time.minute)
            second = str(workout.time.second)

            if len(hour) == 1:
                hour = '0'+hour
            if len(minute) == 1:
                minute = '0'+minute
            if len(second) == 1:
                second = '0'+second

            time = hour+':'+minute+':'+second

            if distance == 0:
                distance = 'N/A'
                units = ''

            context = {
                'title': title,
                'workout': workout,
                'num1_title': 'Sets',
                'num2_title': 'Time',
                'num3_title': 'Distance',
                'num1_value': workout.sets,
                'num2_value': time,
                'num3_value': distance,
                'num3_units': units,
                'referer': referer,
                'update': reverse('edit-c-workout', args=[str(workout.id)]),
                'delete': reverse('delete-c-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


class CWorkoutCreateView(LoginRequiredMixin, CreateView):
    model = CWorkout
    template_name = 'log/workout-form.html'
    form_class = CWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Cardio Workout'
        context['page_title'] = 'New Cardio Workout'
        context['referer'] = reverse('workout-select')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RWorkoutCreateView(LoginRequiredMixin, CreateView):
    model = RWorkout
    template_name = 'log/workout-form.html'
    form_class = RWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Resistance Workout'
        context['page_title'] = 'New Resistance Workout'
        context['referer'] = reverse('workout-select')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WLWorkoutCreateView(LoginRequiredMixin, CreateView):
    model = WLWorkout
    template_name = 'log/workout-form.html'
    form_class = WLWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Weightlifting Workout'
        context['page_title'] = 'New Weightlifting Workout'
        context['referer'] = reverse('workout-select')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CWorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CWorkout
    template_name = 'log/workout-form.html'
    form_class = CWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit ' + self.object.name
        context['page_title'] = self.object.name
        context['referer'] = reverse('c-workout-detail', args=[self.object.id])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False


class RWorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RWorkout
    template_name = 'log/workout-form.html'
    form_class = RWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit ' + self.object.name
        context['page_title'] = self.object.name
        context['referer'] = reverse('r-workout-detail', args=[self.object.id])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False


class WLWorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WLWorkout
    template_name = 'log/workout-form.html'
    form_class = WLWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit ' + self.object.name
        context['page_title'] = self.object.name
        context['referer'] = reverse('wl-workout-detail', args=[self.object.id])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False


class CWorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CWorkout
    template_name = 'log/workout-delete.html'
    success_url = '/workouts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete ' + self.object.name
        context['referer'] = reverse('c-workout-detail', args=[self.object.id])
        return context

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False


class RWorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RWorkout
    template_name = 'log/workout-delete.html'
    success_url = '/workouts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete ' + self.object.name
        context['referer'] = reverse('r-workout-detail', args=[self.object.id])
        return context

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False


class WLWorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WLWorkout
    template_name = 'log/workout-delete.html'
    success_url = '/workouts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete ' + self.object.name
        context['referer'] = reverse('wl-workout-detail', args=[self.object.id])
        return context

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False

