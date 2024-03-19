# models.py
from django.contrib.auth.models import User
from django.db import models

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    patients = models.ManyToManyField('Patient', through='DoctorPatientRelationship')
    # Add other doctor-related fields here

    def __str__(self):
        return self.user.username

class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    # Add any additional fields related to the secretary here

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    appointments = models.ManyToManyField('Appointment', through='PatientAppointmentRelationship')
    # Add other patient-related fields here

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    appointment_time = models.DateTimeField()
    secretary = models.ForeignKey(Secretary, on_delete=models.SET_NULL, null=True)
    # Add other appointment-related fields here

    def __str__(self):
        return f"Appointment at {self.appointment_time}"

class DoctorPatientRelationship(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

class PatientAppointmentRelationship(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

class Analysis(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    analysis_id = models.AutoField(primary_key=True)
    analysis_date = models.DateTimeField(auto_now_add=True)
    textual_diagnostic = models.TextField()
    images_directory = models.CharField(max_length=255)
    # Add other analysis-related fields here

    def __str__(self):
        return f"Analysis ID: {self.analysis_id}"

class AnalysisResult(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    area_curve = models.FileField(upload_to='area_curves/')
    # Add other analysis result fields here

    def __str__(self):
        return f"Result for Analysis ID: {self.analysis.analysis_id}"
