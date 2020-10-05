from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Workout(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=1)
    reps = models.PositiveSmallIntegerField(default=1)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workout-detail', args=[str(self.id)])
