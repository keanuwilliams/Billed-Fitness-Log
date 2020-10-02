from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    workouts = []
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('session-detail', args=[str(self.id)])


class Workout(models.Model):
    name = models.CharField(max_length=100, default="Workout")
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cardio(Workout):
    pass


class Weight(Workout):
    pass


class Resistance(Workout):
    pass
