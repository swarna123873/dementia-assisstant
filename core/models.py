

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class PatientDetails(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    father_name=models.CharField(max_length=100,blank=True, null=True)
    mother_name=models.CharField(max_length=100,blank=True, null=True)
    profession=models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birthplace=models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    schoolname=models.CharField(max_length=100,blank=True, null=True)
    collegename= models.CharField(max_length=255, blank=True, null=True)
    graduationyr=models.CharField(max_length=255, blank=True, null=True)
    degree= models.CharField(max_length=255,blank=True, null=True)
    favactor=models.CharField(max_length=255,blank=True, null=True)
    favactress=models.CharField(max_length=255,blank=True, null=True)
    favmovie=models.CharField(max_length=255,blank=True, null=True)
    favsinger=models.CharField(max_length=255,blank=True, null=True)
    favdesti=models.CharField(max_length=255,blank=True, null=True)
    favcolor=models.CharField(max_length=255,blank=True, null=True)
    favtimepass=models.CharField(max_length=255,blank=True, null=True)
    favfood=models.CharField(max_length=255,blank=True, null=True)
    favfruit=models.CharField(max_length=255,blank=True, null=True)
    def __str__(self):
        return self.name

class PatientPhoto(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient_photos/')
    description = models.CharField(max_length=255, blank=True)



    def __str__(self):
        return f"{self.patient.name} - {self.description}"
class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.relation})"
CATEGORY_CHOICES = [
    ('family', 'Family'),
    ('friends', 'Friends'),
    ('other', 'Other'),
]

class FacePhoto(models.Model):
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='faces/')
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} - {self.description}"  
class SchoolPhoto(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='school_photos/')

class CollegePhoto(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='college_photos/')

class MemoryPhoto(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='memory_photos/')
    description = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"{self.patient} - {self.description}"  
class MedicalReminder(models.Model):
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    time = models.CharField(max_length=5) 

class DailyLifeReminder(models.Model):
    ACTIVITY_CHOICES = [
        ("Bathing 🚿", "Bathing 🚿"),
        ("Sleeping 💤", "Sleeping 💤"),
        ("Drinking Water 💧", "Drinking Water 💧"),
        ("Breakfast 🍳", "Breakfast 🍳"),
        ("Lunch 🍛", "Lunch 🍛"),
        ("Dinner 🍽️", "Dinner 🍽️"),
        ("Skincare 💆", "Skincare 💆"),
        ("Watering Plants 🌿", "Watering Plants 🌿"),
        ("Reading Books 📚", "Reading Books 📚"),
        ("Arranging Room 🧹", "Arranging Room 🧹"),
    ]
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    time = models.CharField(max_length=5) 
    def task_display(self):
        return f"{self.activity} 🧠"