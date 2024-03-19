#url.py
from django.urls import path
from . import views as myapp_views  # Rename the import to avoid conflicts

urlpatterns = [
    path('', myapp_views.home, name="home"),
    path('register/doctor/', myapp_views.register_doctor, name='register_doctor'),
    path('register/secretary/', myapp_views.register_secretary, name='register_secretary'),
    path('login/', myapp_views.my_login, name="my_login"),
    path('dashboard/', myapp_views.dashboard, name="dashboard"),
    path('logout/', myapp_views.user_logout, name='user_logout'),
    path('make_appointment/', myapp_views.make_appointment, name='make_appointment'),
    path('add_patient/', myapp_views.add_patient, name='add_patient'),
    path('view_patient/<int:patient_id>/', myapp_views.view_patient, name='view_patient'),
    path('load_images/<int:patient_id>/', myapp_views.load_images, name='load_images'),
    path('write_diagnostic/<int:patient_id>/', myapp_views.write_diagnostic, name='write_diagnostic'),
    path('secretary_dashboard/', myapp_views.secretary_dashboard, name='secretary_dashboard'),
    path('doctor_dashboard/', myapp_views.doctor_dashboard, name='doctor_dashboard'),
]