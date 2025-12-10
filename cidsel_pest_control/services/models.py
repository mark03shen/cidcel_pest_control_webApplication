# services/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class TechnicianStatus(models.Model):
    technician = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="status"
    )
    last_active = models.DateTimeField(auto_now=True)

    def is_online(self):
        return timezone.now() - self.last_active < timedelta(minutes=2)

# class Appointment(models.Model):
#     customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     appointment_date = models.DateTimeField()
#     status = models.CharField(max_length=20, default='Pending')
    

# this is for the Feedback interface
class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('General Pest Control', 'General Pest Control'),
        ('Termite Spot Treatment', 'Termite Spot Treatment'), 
        ('Termite Comprehensive', 'Termite Comprehensive'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    rating = models.PositiveIntegerField(default=0)  # ⭐️ New rating field (1 to 5)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.category} - {self.rating}⭐"

#--- this is for customer notification
class CustomerNotification(models.Model):
    appointment = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer Notification from {self.client_name}"


#--- this for Book_appointment.html---#
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Done', 'Done'),
    ]

    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    land_use_category = models.CharField(
        max_length=50,
        choices=[
            ("Industrial", "Industrial"),
            ("Residential", "Residential"),
            ("Institutional", "Institutional"),
            ("Commercial", "Commercial"),
        ],
        default="Residential"
    )
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    job_location = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True)
    barangay = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True)
    house_number = models.CharField(max_length=50, blank=True)

    total_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    contract_period = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50)
    receipt = models.ImageField(upload_to="receipts/", blank=True, null=True)
    
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("in-progress", "In Progress"), ("completed", "Completed")],
        default='Pending' 
    )

    def __str__(self):
        return f"{self.client_name} - {self.service} on {self.date}"
    
    # ✅ Auto-calculate price logic
    def calculate_price(self):
        if self.service == "General Pest Control":
            return 3800
        elif self.service == "Termite Spot Treatment":
            return 2000
        elif self.service == "Termite Comprehensive":
            if self.contract_period == "1 year":
                return 2500
            elif self.contract_period == "2 years":
                return 4500
        return None  # fallback

    # ✅ Override save to always fill estimated_price
    def save(self, *args, **kwargs):
        if not self.estimated_price:  # only set if empty
            self.estimated_price = self.calculate_price() 
        super().save(*args, **kwargs)

#--- for payment receipt upload
class Receipt(models.Model):
    appointment = models.ForeignKey("Appointment", on_delete=models.CASCADE, related_name="receipts")
    image = models.ImageField(upload_to="receipts/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.appointment.client_name} - {self.appointment.payment_method}"


#--- for customer faqs message
class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    is_admin = models.BooleanField(default=False)  # True if admin sent it
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'Admin' if self.is_admin else self.sender.username}: {self.message[:30]}"


#--- for invertory item
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Materials', 'Materials'),
        ('Equipment', 'Equipment'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    measurement = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    is_used = models.BooleanField(default=False)


    def status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity < 50:
            return "Low Stock"
        return "Available"

    def __str__(self):
        return self.name




#--- for Technician content ------

class VerificationAssignment(models.Model):
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    # Approval state
    approval_status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved')],
        default='pending'
    )

    # Visit stage (separate from approval)
    progress_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    inventory_updated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.technician.username} - {self.appointment.client_name}"


class TechnicianNotification(models.Model):
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.technician.username}: {self.message}"


class TechnicianProgress(models.Model):
    assignment = models.ForeignKey(VerificationAssignment, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="technician_progress/")
    description = models.TextField()
    progress_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.technician} - {self.progress_status}"
    


#--- for customer profile
def user_directory_path(instance, filename):
    # Upload to: MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, default='profile_pics/default.png')

    def __str__(self):
        return f"{self.user.username} Profile"

# Auto-create or update profile when user is created
def user_profile_path(instance, filename):
    # store images under media/profile_pics/<username>/
    return f'profile_pics/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_image_url(self):
        if self.image:
            return self.image.url
        from django.conf import settings
        return settings.STATIC_URL + 'default_pic.png'


#--- for technician photo documentation
class PhotoDocumentation(models.Model): 
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    image = models.ImageField(upload_to='photo_documentation/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.technician.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    
#--- for admin upload  to post in gallery
class UploadedPhoto(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General Pest Control"),
        ("termite_comprehensive", "Termite Comprehensive"),
        ("termite_spot", "Termite Spot Treatment"),
    ]

    photo = models.ImageField(upload_to="uploads/photos/")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="general")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_category_display()} - {self.photo.name} uploaded by {self.uploaded_by}"