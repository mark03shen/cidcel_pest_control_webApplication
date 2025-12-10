# services/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from .models import Appointment
from .models import Product
from .models import CustomUser

from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''  # Remove help texts


# This is for the APPIONTMENT BUTTON
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


#--- this is for Inventory---#
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']  # measurement removed from form

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        # Server-side enforcement: auto-assign measurement for Materials
        if category == "Materials":
            cleaned_data['measurement'] = "L"
        else:
            cleaned_data['measurement'] = None

        return cleaned_data
    
#--- for technician signUp and logIn
class TechnicianSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_technician = True
        if commit:
            user.save()
        return user

#--- for customer profile 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    
#--- for technician photo documentation
from .models import PhotoDocumentation

class PhotoDocumentationForm(forms.ModelForm):
    class Meta:
        model = PhotoDocumentation
        fields = ['image', 'description']

#--- for uploading pictures from admin to customer dashboard
from .models import UploadedPhoto

class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = UploadedPhoto
        fields = ['photo', 'category']