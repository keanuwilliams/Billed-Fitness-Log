from django import forms
from flatpickr import DatePickerInput
from .models import Workout


class WorkoutForm(forms.ModelForm):
    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = Workout
        fields = ['name', 'date']
