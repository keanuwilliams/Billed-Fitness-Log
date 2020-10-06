from django.contrib import admin
from .models import CWorkout, RWorkout, WLWorkout


class CWorkoutAdmin(admin.ModelAdmin):
    name = 'Cardio Workout'
    list_display = ('name', 'date', 'user',)


class RWorkoutAdmin(admin.ModelAdmin):
    name = 'Resistance Workout'
    list_display = ('name', 'date', 'user',)


class WLWorkoutAdmin(admin.ModelAdmin):
    name = 'Weightlifting Workout'
    list_display = ('name', 'date', 'user',)


admin.site.register(CWorkout, CWorkoutAdmin)
admin.site.register(RWorkout, RWorkoutAdmin)
admin.site.register(WLWorkout, WLWorkoutAdmin)
