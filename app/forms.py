# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Driver

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class DriverSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class DriverRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    license_plate_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'phone_number', 'license_plate_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name'].split()[0]
        user.last_name = self.cleaned_data['name'].split()[1]
        if commit:
            user.save()
            driver = Driver.objects.create(user=user, name=self.cleaned_data['name'], phone_number=self.cleaned_data['phone_number'], license_plate_number=self.cleaned_data['license_plate_number'])
        return user
    


