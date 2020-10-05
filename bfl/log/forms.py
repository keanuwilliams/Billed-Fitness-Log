from django import forms
from flatpickr import DatePickerInput
from .models import Workout


class WorkoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs['min'] = 0
        self.fields['sets'].widget.attrs['min'] = 1
        self.fields['reps'].widget.attrs['min'] = 1

    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = Workout
        fields = ['name', 'date', 'sets', 'reps', 'weight']
