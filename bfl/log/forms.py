from django import forms
from flatpickr import DatePickerInput
from .models import WLWorkout, CWorkout, RWorkout


class CWorkoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CWorkoutForm, self).__init__(*args, **kwargs)
        self.fields['sets'].widget.attrs['min'] = 1
        self.fields['distance'].widget.attrs['min'] = 0

    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = CWorkout
        fields = ['name', 'date', 'sets', 'time', 'distance']


class RWorkoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RWorkoutForm, self).__init__(*args, **kwargs)
        self.fields['sets'].widget.attrs['min'] = 1
        self.fields['reps'].widget.attrs['min'] = 1

    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = RWorkout
        fields = ['name', 'date', 'sets', 'reps', 'resistance']


class WLWorkoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WLWorkoutForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs['min'] = 0
        self.fields['sets'].widget.attrs['min'] = 1
        self.fields['reps'].widget.attrs['min'] = 1

    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = WLWorkout
        fields = ['name', 'date', 'sets', 'reps', 'weight']
