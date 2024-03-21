#forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from .models import Secretary, Doctor


class DoctorRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=30, label='Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    email = forms.EmailField(max_length=254, label='Email', help_text='Required. Inform a valid email address.')
    phone = forms.CharField(max_length=15, label='Phone Number')

    class Meta:
        model = User
        fields = ('username', 'name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        if commit:
            user.save()
            doctor = Doctor.objects.create(user=user)
            doctor.save()
        return user


class SecretaryRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=30, label='Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    email = forms.EmailField(max_length=254, label='Email', help_text='Required. Inform a valid email address.')
    phone = forms.CharField(max_length=15, label='Phone Number')
    assigned_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Assigned Doctor', required=False)

    class Meta:
        model = User
        fields = ('username', 'name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'secretary'  # Assign the role here if needed

        if commit:
            user.save()
            assigned_doctor = self.cleaned_data.get('assigned_doctor')
            # Create and associate a Secretary object with the user
            secretary_instance = Secretary.objects.create(user=user)
            secretary_instance.save()

        return user


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate



class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email", widget=EmailInput())
    password = forms.CharField(label="Password", widget=PasswordInput())

    class Meta:
        fields = ['email', 'password']  # Define the field order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override the default fields with custom fields
        self.fields['username'] = self.fields.pop('username', None)
        self.fields['password'] = self.fields.pop('password', None)
from .models import Patient, Appointment, Analysis



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone_number']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time']
        exclude = ['secretary']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['doctor', 'patient', 'textual_diagnostic', 'images_directory']
        widgets = {
            'doctor': forms.HiddenInput(),  # This field will be populated in the view
            'patient': forms.HiddenInput(),  # This field will be populated in the view
        }