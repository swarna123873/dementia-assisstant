from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import PatientDetails, PatientPhoto
from django.forms import modelformset_factory
from .models import EmergencyContact
from .models import FacePhoto
from .models import SchoolPhoto, CollegePhoto, MemoryPhoto
from .models import MedicalReminder, DailyLifeReminder
class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']



class PatientDetailsForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = PatientDetails
        fields = ['name', 'age', 'father_name', 'mother_name', 'profession', 'address', 'birthplace', 'birthdate','schoolname','collegename','graduationyr','degree','favactor','favactress','favmovie','favsinger','favdesti','favcolor','favtimepass','favfood','favfruit']

class PatientPhotoForm(forms.ModelForm):
    class Meta:
        model = PatientPhoto
        fields = ['image', 'description']



PatientPhotoFormSet = modelformset_factory(PatientPhoto, form=PatientPhotoForm, extra=2)
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relation']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'relation': forms.TextInput(attrs={'placeholder': 'Relation'}),
        }

EmergencyContactFormSet = modelformset_factory(
    EmergencyContact,
    form=EmergencyContactForm,
    extra=5,
    max_num=5,
    can_delete=True
)
class FacePhotoForm(forms.ModelForm):
    class Meta:
        model = FacePhoto
        fields = ['image', 'description']
class SchoolPhotoForm(forms.ModelForm):
    class Meta:
        model = SchoolPhoto
        fields = ['image']

class CollegePhotoForm(forms.ModelForm):
    class Meta:
        model = CollegePhoto
        fields = ['image']

class MemoryPhotoForm(forms.ModelForm):
    class Meta:
        model = MemoryPhoto
        fields = ['image', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Add description here'}),
        }


class MedicalReminderForm(forms.ModelForm):
    class Meta:
        model = MedicalReminder
        fields = ['medicine_name', 'dosage', 'time']
        widgets = {
            
        'time': forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'HH:MM (24-hour)',
        'pattern': '([01][0-9]|2[0-3]):[0-5][0-9]',
        'title': 'Enter time in 24-hour format HH:MM',
    }),
}
        

class DailyReminderForm(forms.ModelForm):
    class Meta:
        model =DailyLifeReminder
        fields = ['activity', 'time']
        widgets = {
            'time': forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'HH:MM (24-hour)',
        'pattern': '([01][0-9]|2[0-3]):[0-5][0-9]',
        'title': 'Enter time in 24-hour format HH:MM',
    }),
        }

SchoolPhotoFormSet = modelformset_factory(SchoolPhoto, form=SchoolPhotoForm, extra=6, can_delete=True)
CollegePhotoFormSet = modelformset_factory(CollegePhoto, form=CollegePhotoForm, extra=6, can_delete=True)
MemoryPhotoFormSet = modelformset_factory(MemoryPhoto, form=MemoryPhotoForm, extra=5, can_delete=True)  