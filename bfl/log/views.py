from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def my_workouts(request):

    context = {
        'title': 'My Workouts',
    }
    
    return render(request, 'log/my-workout.html', context)
