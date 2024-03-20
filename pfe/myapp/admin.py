#admin.py 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Secretary
from django.contrib.auth.models import User

# Define inline admin classes for Doctor and Secretary models
class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor'

class SecretaryInline(admin.StackedInline):
    model = Secretary
    can_delete = False
    verbose_name_plural = 'Secretary'

# Extend the UserAdmin class to include Doctor and Secretary models as inlines
class CustomUserAdmin(UserAdmin):
    inlines = (DoctorInline, SecretaryInline)

# Define a custom admin class for Secretary
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'assigned_doctor')
    list_filter = ('assigned_doctor',)  
    search_fields = ('user__username', 'phone')  

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register Doctor and Secretary models
admin.site.register(Doctor)
admin.site.register(Secretary, SecretaryAdmin)
from .models import Doctor, Secretary, Patient, Appointment, DoctorPatientRelationship, PatientAppointmentRelationship, Analysis, AnalysisResult

# Register all models that you want to manage through the Django admin interface
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorPatientRelationship)
admin.site.register(PatientAppointmentRelationship)
admin.site.register(Analysis)
admin.site.register(AnalysisResult)