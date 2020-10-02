from django import forms
from flatpickr import DatePickerInput
from .models import Session


class SessionForm(forms.ModelForm):
    date = forms.DateField(widget=DatePickerInput(options={'maxDate': 'today'}))

    class Meta:
        model = Session
        fields = ['name', 'date']
