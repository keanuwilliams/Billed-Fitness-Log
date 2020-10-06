from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import datetime


class CWorkout(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=1)
    distance = models.FloatField(default=0)
    time = models.TimeField(default=datetime.time(0, 0, 0))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('c-workout-detail', args=[str(self.id)])


class RWorkout(models.Model):
    R_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('D', 'Difficult'),
        ('A', 'Advanced'),
    )

    name = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=1)
    reps = models.PositiveSmallIntegerField(default=1)
    resistance = models.CharField(max_length=1, choices=R_CHOICES, default='E')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('r-workout-detail', args=[str(self.id)])


class WLWorkout(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=1)
    reps = models.PositiveSmallIntegerField(default=1)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wl-workout-detail', args=[str(self.id)])
