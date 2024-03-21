# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm, DoctorRegistrationForm, SecretaryRegistrationForm, AppointmentForm, PatientForm, AnalysisForm
from .models import Doctor, Secretary, Patient, Analysis
from .forms import LoginForm


def home(request):
    context = {}
    return render(request, "myapp/home.html", context)

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            doctor_group, created = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)
            messages.success(request, "Doctor registration successful. Please log in.")
            return redirect('my_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DoctorRegistrationForm()

    context = {'RegistrationForm': form}
    return render(request, "myapp/register-doctor.html", context)

def register_secretary(request):
    if request.method == 'POST':
        form = SecretaryRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            secretary_group, created = Group.objects.get_or_create(name='Secretary')
            user.groups.add(secretary_group)
            messages.success(request, "Secretary registration successful. Please log in.")
            return redirect('my_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SecretaryRegistrationForm()

    context = {'RegistrationForm': form}
    return render(request, "myapp/register-secretary.html", context)
from django.contrib.auth.models import Group

def my_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("admin:index")  # Redirect superusers to admin panel
                elif user.groups.filter(name='Secretary').exists():
                    return redirect(reverse("secretary_dashboard"))  # Redirect secretaries to secretary dashboard
                elif user.groups.filter(name='Doctor').exists():
                    return redirect(reverse("doctor_dashboard"))  # Redirect doctors to doctor dashboard
                else:
                    return redirect("dashboard")  # Redirect regular users to dashboard
            else:
                # If authentication fails, display an error message
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    context = {'loginform': form}
    return render(request, "myapp/my_login.html", context)

@login_required(login_url="my_login")
def dashboard(request):
    return render(request, "myapp/dashboard.html")

@login_required(login_url="my_login")
def secretary_dashboard(request):
    return render(request, "myapp/secretary_dashboard.html")

@login_required(login_url="my_login")
def doctor_dashboard(request):
    return render(request, "myapp/doctor_dashboard.html")
@login_required
def dashboard(request):
    context = {}  # Add any context data you want to pass to the template
    return render(request, "myapp/dashboard.html", context)

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.secretary = request.user.secretary
            appointment.save()
            messages.success(request, 'Appointment successfully created!')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    
    context = {'form': form}
    return render(request, 'myapp/make_appointment.html', context)

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, 'Patient successfully added!')
            return redirect('dashboard')
    else:
        form = PatientForm()
    
    context = {'form': form}
    return render(request, 'myapp/add_patient.html', context)

@login_required
@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    analyses = Analysis.objects.filter(patient=patient)
    context = {'patient': patient, 'analyses': analyses}
    return render(request, 'myapp/view_patient.html', context)

@login_required
def load_images(request, patient_id):
    # Logic to load patient images
    pass

@login_required
def write_diagnostic(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            diagnostic = form.save(commit=False)
            diagnostic.patient = patient
            diagnostic.doctor = request.user.doctor
            diagnostic.save()
            messages.success(request, 'Diagnostic successfully added!')
            return redirect('view_patient', patient_id=patient_id)
    else:
        form = AnalysisForm()
    
    context = {'form': form, 'patient': patient}
    return render(request, 'myapp/write_diagnostic.html', context)
def user_logout(request):
     logout(request)
     return redirect("home")
