from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        """
        Used to overwrite the focus of the cursor when the user first opens the page.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['first_name'].widget.attrs.update({'autofocus': True})

    def clean_email(self):
        """
        Checks the email if it is unique.
        """
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)  # Try to find a user with the email the user entered.
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('The email address is already in use by another user.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def clean_email(self):
        """
        Checks if the user's email is unique.
        """
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)  # Try to find a user with the email the user entered.
        except User.DoesNotExist:
            return email
        else:
            if user == self.instance:
                return email
            else:
                # Raise the validation error if the user's entered email is not the same as the user's current email
                raise forms.ValidationError('This email address is already in use.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class EditWorkoutInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['weight', 'goal_weight']


class EditUnitsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['weight_units', 'distance_units']
