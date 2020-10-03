from django.contrib import admin
from .models import Workout


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user',)


admin.site.register(Workout, WorkoutAdmin)
