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


@login_required
def my_workouts(request):

    context = {
        'title': 'My Workouts',
    }
    return render(request, 'log/my-workout.html', context)


class CWorkoutListView(ListView, LoginRequiredMixin):
    model = CWorkout
    template_name = 'log/workout-list.html'
    ordering = '-date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Cardio'
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
    template_name = 'log/workout-list.html'
    ordering = '-date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Resistance'
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
    template_name = 'log/workout-list.html'
    ordering = '-date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Weightlifting'
        context['category'] = 'WEIGHTLIFTING'
        context['th_1'] = 'Weight'
        context['th_2'] = 'Sets'
        context['th_3'] = 'Reps'
        return context

    def get_queryset(self):
        queryset = WLWorkout.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


@login_required
def select_workouts(request):
    context = {
        'title': 'Select Workout Type',
    }
    return render(request, 'log/workout-select.html', context)


@login_required
def wl_workout_detail(request, pk):
    try:
        workout = WLWorkout.objects.get(pk=pk)
        related = WLWorkout.objects.exclude(pk=workout.pk).filter(name=workout.name,
                                                                  user=workout.user).order_by('-date')[:5]
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
                        or (any(char.isdigit() for char in request.META.get('HTTP_REFERER'))
                            and '/weightlifting/' in request.META.get('HTTP_REFERER')) \
                        or '/delete/' in request.META.get('HTTP_REFERER'):
                    referer = reverse('my-workouts')
                else:
                    referer = request.META.get('HTTP_REFERER')
            else:
                referer = reverse('my-workouts')

            context = {
                'title': title,
                'category': 'WEIGHTLIFTING',
                'workout': workout,
                'related': related,
                'num1_title': 'Sets',
                'num2_title': 'Reps',
                'num3_title': 'Weight',
                'num1_value': workout.sets,
                'num2_value': workout.reps,
                'num3_value': workout.weight,
                'num3_units': workout.user.profile.weight_units,
                'referer': referer,
                'update': reverse('edit-wl-workout', args=[str(workout.id)]),
                'duplicate': reverse('duplicate-wl-workout', args=[str(workout.id)]),
                'delete': reverse('delete-wl-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


@login_required
def r_workout_detail(request, pk):
    try:
        workout = RWorkout.objects.get(pk=pk)
        related = RWorkout.objects.exclude(pk=workout.pk).filter(name=workout.name,
                                                                 user=workout.user).order_by('-date')[:5]
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
                        or (any(char.isdigit() for char in request.META.get('HTTP_REFERER'))
                            and '/resistance/' in request.META.get('HTTP_REFERER')) \
                        or '/delete/' in request.META.get('HTTP_REFERER'):
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
                'category': 'RESISTANCE',
                'workout': workout,
                'related': related,
                'num1_title': 'Sets',
                'num2_title': 'Reps',
                'num3_title': 'Resistance',
                'num1_value': workout.sets,
                'num2_value': workout.reps,
                'num3_value': resistance,
                'num3_units': '',
                'referer': referer,
                'update': reverse('edit-r-workout', args=[str(workout.id)]),
                'duplicate': reverse('duplicate-r-workout', args=[str(workout.id)]),
                'delete': reverse('delete-r-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


@login_required
def c_workout_detail(request, pk):
    try:
        workout = CWorkout.objects.get(pk=pk)
        related = CWorkout.objects.exclude(pk=workout.pk).filter(name=workout.name,
                                                                 user=workout.user).order_by('-date')[:5]
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
                        or (any(char.isdigit() for char in request.META.get('HTTP_REFERER'))
                            and '/cardio/' in request.META.get('HTTP_REFERER')) \
                        or '/delete/' in request.META.get('HTTP_REFERER'):
                    referer = reverse('my-workouts')
                else:
                    referer = request.META.get('HTTP_REFERER')
            else:
                referer = reverse('my-workouts')

            distance = workout.distance
            units = workout.user.profile.distance_units

            if distance == 0:
                distance = 'N/A'
                units = ''

            hour = str(workout.time.hour)
            minute = str(workout.time.minute)
            second = str(workout.time.second)

            if len(hour) == 1:
                hour = '0' + hour
            if len(minute) == 1:
                minute = '0' + minute
            if len(second) == 1:
                second = '0' + second

            time = hour + ':' + minute + ':' + second

            context = {
                'title': title,
                'category': 'CARDIO',
                'workout': workout,
                'related': related,
                'num1_title': 'Sets',
                'num2_title': 'Time',
                'num3_title': 'Distance',
                'num1_value': workout.sets,
                'num2_value': time,
                'num3_value': distance,
                'num3_units': units,
                'referer': referer,
                'update': reverse('edit-c-workout', args=[str(workout.id)]),
                'duplicate': reverse('duplicate-c-workout', args=[str(workout.id)]),
                'delete': reverse('delete-c-workout', args=[str(workout.id)]),
            }
            return render(request, 'log/workout-detail.html', context)


@login_required
def c_workout_duplicate(request, pk):
    try:
        workout = CWorkout.objects.get(pk=pk)
    except CWorkout.DoesNotExist:
        raise Http404
    else:
        if workout.user != request.user:
            messages.warning(request, 'You do not have access to that workout.')
            return redirect('my-workouts')
        else:
            workout.pk = None
            if request.method == "POST":
                workout.save()
                messages.success(request, 'Workout successfully duplicated.')
                return redirect('edit-c-workout', workout.pk)
            context = {
                'title': 'Deactivate',
                'workout': workout,
                'referer': request.META.get('HTTP_REFERER'),
            }
            return render(request, 'log/workout-duplicate.html', context)


@login_required
def r_workout_duplicate(request, pk):
    try:
        workout = RWorkout.objects.get(pk=pk)
    except RWorkout.DoesNotExist:
        raise Http404
    else:
        if workout.user != request.user:
            messages.warning(request, 'You do not have access to that workout.')
            return redirect('my-workouts')
        else:
            workout.pk = None
            if request.method == "POST":
                workout.save()
                messages.success(request, 'Workout successfully duplicated.')
                return redirect('edit-r-workout', workout.pk)
            context = {
                'title': 'Deactivate',
                'workout': workout,
                'referer': request.META.get('HTTP_REFERER'),
            }
            return render(request, 'log/workout-duplicate.html', context)


@login_required
def wl_workout_duplicate(request, pk):
    try:
        workout = WLWorkout.objects.get(pk=pk)
    except WLWorkout.DoesNotExist:
        raise Http404
    else:
        if workout.user != request.user:
            messages.warning(request, 'You do not have access to that workout.')
            return redirect('my-workouts')
        else:
            workout.pk = None
            if request.method == "POST":
                workout.save()
                messages.success(request, 'Workout successfully duplicated.')
                return redirect('edit-wl-workout', workout.pk)
            context = {
                'title': 'Deactivate',
                'workout': workout,
                'referer': request.META.get('HTTP_REFERER'),
            }
            return render(request, 'log/workout-duplicate.html', context)


class CWorkoutCreateView(LoginRequiredMixin, CreateView):
    model = CWorkout
    template_name = 'log/workout-form.html'
    form_class = CWorkoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Cardio Workout'
        context['page_title'] = 'New Cardio Workout'
        context['referer'] = reverse('workout-select')
        context['cardio'] = True
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
        context['cardio'] = True
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
