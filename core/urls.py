from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('patient/', views.patient_view, name='patient'),
    path('caregiver/', views.caregiver_view, name='caregiver'),
    path('about/', views.about_view, name='about'),
    path('about1/', views.about1_view, name='about1'),
    path('upload-all/<int:patient_id>/', views.upload_patient_details_and_photos, name='upload_patient_details_and_photos'),
    path('caregiver/', views.caregiver_view, name='caregiver'),
    path('know_about_yourself/', views.know_about_yourself, name='know_about_yourself'),
    path('upload-emergency/', views.upload_emergency_contacts, name='upload_emergency_contacts'),
    path('emergency/', views.emergency_view, name='emergency_view'),
    path('upload_faces/', views.upload_faces, name='upload_faces'),
    path('recognize_faces/', views.recognize_faces, name='recognize_faces'),
    path('set-alarms/', views.set_alarms, name='set_alarms'),
    path('see_reminders/', views.see_reminders, name='see_reminders'),
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('get-response/', views.get_chat_response, name='get_chat_response'),

]
