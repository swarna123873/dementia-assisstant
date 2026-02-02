from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from .forms import RegisterForm
from .models import CustomUser
from .models import PatientDetails,PatientPhoto
from .forms import PatientDetailsForm,PatientPhotoFormSet
from .forms import EmergencyContactFormSet
from .models import EmergencyContact
from .models import FacePhoto
from .forms import FacePhotoForm
from django.forms import modelformset_factory
from .models import SchoolPhoto, CollegePhoto, MemoryPhoto
from .forms import SchoolPhotoFormSet, CollegePhotoFormSet, MemoryPhotoFormSet
from django.shortcuts import get_object_or_404
from .forms import MedicalReminderForm, DailyReminderForm
from .models import MedicalReminder, DailyLifeReminder
import csv
import os
from django.http import JsonResponse
from django.conf import settings

@never_cache
def home(request):
    return render(request, 'login.html')
@never_cache
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@never_cache
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient')
            elif user.role == 'caregiver':
                return redirect('caregiver')
    return redirect('home')

def patient_view(request):
    return render(request, 'patient.html')

def caregiver_view(request):
    return render(request, 'caregiver.html')

def about_view(request):
    return render(request, 'about.html')
def about1_view(request):
    return render(request, 'about1.html')
def upload_patient_details_and_photos(request, patient_id):
    patient = get_object_or_404(PatientDetails, id=patient_id)

    # Patient form and general photos formset (2 photos with description)
    patient_form = PatientDetailsForm(request.POST or None, instance=patient)
    photo_formset = PatientPhotoFormSet(request.POST or None, request.FILES or None, queryset=PatientPhoto.objects.filter(patient=patient))

    # School/College/Memory formsets
    school_formset = SchoolPhotoFormSet(request.POST or None, request.FILES or None, queryset=SchoolPhoto.objects.filter(patient=patient), prefix='school')
    college_formset = CollegePhotoFormSet(request.POST or None, request.FILES or None, queryset=CollegePhoto.objects.filter(patient=patient), prefix='college')
    memory_formset = MemoryPhotoFormSet(request.POST or None, request.FILES or None, queryset=MemoryPhoto.objects.filter(patient=patient), prefix='memory')

    if request.method == 'POST':
        if patient_form.is_valid() and photo_formset.is_valid() and school_formset.is_valid() and college_formset.is_valid() and memory_formset.is_valid():
            # Save patient details
            patient = patient_form.save()

            # Save general photos
            photos = photo_formset.save(commit=False)
            for photo in photos:
                photo.patient = patient
                photo.save()

            # Save categorized photos
            for form in school_formset.save(commit=False):
                form.patient = patient
                form.save()
            for form in college_formset.save(commit=False):
                form.patient = patient
                form.save()
            for form in memory_formset.save(commit=False):
                form.patient = patient
                form.save()

            # Handle deletions
            for obj in photo_formset.deleted_objects:
                obj.delete()
            for obj in school_formset.deleted_objects:
                obj.delete()
            for obj in college_formset.deleted_objects:
                obj.delete()
            for obj in memory_formset.deleted_objects:
                obj.delete()

            return redirect('upload_patient_details_and_photos', patient_id=patient.id)

    return render(request, 'upload_patient_details.html', {
        'form': patient_form,
        'formset': photo_formset,
        'school_formset': school_formset,
        'college_formset': college_formset,
        'memory_formset': memory_formset,
        'patient': patient,
    })

def know_about_yourself(request):
    patient = PatientDetails.objects.first()

    # Old photos with descriptions
    photos = PatientPhoto.objects.filter(patient=patient)

    # New categorized photos
    school_photos = SchoolPhoto.objects.filter(patient=patient)
    college_photos = CollegePhoto.objects.filter(patient=patient)
    memory_photos = MemoryPhoto.objects.filter(patient=patient)

    return render(request, 'know_about_yourself.html', {
        'patient': patient,
        'photos': photos,  # Old PatientPhoto
        'school_photos': school_photos,
        'college_photos': college_photos,
        'memory_photos': memory_photos,
    })
def caregiver_view(request):
    patient = PatientDetails.objects.first()
    return render(request, 'caregiver.html', {'patient': patient})
def upload_emergency_contacts(request):
    contacts = EmergencyContact.objects.all()
    if request.method == 'POST':
        formset = EmergencyContactFormSet(request.POST, queryset=contacts)
        if formset.is_valid():
            formset.save()
            return redirect('emergency_view')
    else:
        formset = EmergencyContactFormSet(queryset=contacts)

    return render(request, 'upload_emergency.html', {'formset': formset})

def emergency_view(request):
    contacts = EmergencyContact.objects.all()
    return render(request, 'emergency.html', {'contacts': contacts})
def upload_faces(request):
    FacePhotoFormSet = modelformset_factory(FacePhoto, form=FacePhotoForm, extra=6)
    if request.method == 'POST':
        formsets = {}
        for category in ['family', 'friends', 'other']:
            formsets[category] = FacePhotoFormSet(
                request.POST, request.FILES,
                queryset=FacePhoto.objects.filter(category=category),
                prefix=category
            )
        if all(formset.is_valid() for formset in formsets.values()):
            for category, formset in formsets.items():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.category = category
                    instance.save()
            return redirect('recognize_faces')
    else:
        formsets = {
            category: FacePhotoFormSet(
                queryset=FacePhoto.objects.filter(category=category),
                prefix=category
            ) for category in ['family', 'friends', 'other']
        }
    return render(request, 'upload_faces.html', {'formsets': formsets})

def recognize_faces(request):
    photos = {
        category: FacePhoto.objects.filter(category=category)
        for category in ['family', 'friends', 'other']
    }
    return render(request, 'recognize_faces.html', {'photos': photos})
def set_alarms(request):
    if request.method == 'POST':
        if 'add_medical' in request.POST:
            med_form = MedicalReminderForm(request.POST)
            if med_form.is_valid():
                med_form.save()
        elif 'add_daily' in request.POST:
            daily_form = DailyReminderForm(request.POST)
            if daily_form.is_valid():
                daily_form.save()
        elif 'delete_med' in request.POST:
            med_id = request.POST.get('delete_med')
            MedicalReminder.objects.filter(id=med_id).delete()
        elif 'delete_daily' in request.POST:
            daily_id = request.POST.get('delete_daily')
            DailyLifeReminder.objects.filter(id=daily_id).delete()
        return redirect('set_alarms')
    
    med_form = MedicalReminderForm()
    daily_form = DailyReminderForm()
    med_reminders = MedicalReminder.objects.all()
    daily_reminders = DailyLifeReminder.objects.all()

    return render(request, 'set_alarms.html', {
        'med_form': med_form,
        'daily_form': daily_form,
        'med_reminders': med_reminders,
        'daily_reminders': daily_reminders,
    })
def see_reminders(request):
    medical_reminders = MedicalReminder.objects.all()
    daily_reminders =  DailyLifeReminder.objects.all()
    return render(request, 'see_reminders.html', {
        'medical_reminders': medical_reminders,
        'daily_reminders': daily_reminders
    })
chat_data = {}

csv_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'newdata.csv')
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = row['question'].strip().lower()
        response = row['response'].strip()
        
        chat_data[question] = response

def chatbot_page(request):
    return render(request, 'chatbot.html')

def get_chat_response(request):
    if request.method == "POST":
        question = request.POST.get("message", "").strip().lower()
        response = chat_data.get(question, "Sorry, I don't understand that yet.")
        return JsonResponse({'response': response})



