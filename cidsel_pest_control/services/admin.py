from django.contrib import admin
from .models import Appointment
from .models import Product
from .models import Feedback
from .models import Profile
from .models import UploadedPhoto
from .models import ChatMessage


#--- for customer appointment booking
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'job_location', 'service', 'date', 'time', 'payment_method')
    search_fields = ('client_name', 'email', 'mobile', 'job_location', 'service')
    list_filter = ('job_location', 'service', 'payment_method', 'date')


#--- for admin invertory
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'status', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)


#--- for customer feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'rating', 'message', 'submitted_at')
    list_filter = ('category', 'rating', 'submitted_at')
    search_fields = ('user__username', 'message', 'category')
    ordering = ('-submitted_at',)
    
#--- for profile picture upload
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username', 'user__email')
    
    
#--- for technician photo documentation
from .models import PhotoDocumentation

@admin.register(PhotoDocumentation)
class PhotoDocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'technician', 'description', 'created_at')
    list_filter = ('created_at', 'technician')
    search_fields = ('technician__username', 'description')
    ordering = ('-created_at',)


#--- for uploading photos from admin to customer dashboard
@admin.register(UploadedPhoto)
class UploadedPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('uploaded_by__username', )
    ordering = ('-uploaded_at',)
    
#--- for customer faqs message
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'is_admin', 'short_message', 'timestamp')
    list_filter = ('is_admin', 'timestamp')
    search_fields = ('sender__username', 'message')
    ordering = ('-timestamp',)

    def short_message(self, obj):
        return (obj.message[:50] + "...") if len(obj.message) > 50 else obj.message
    short_message.short_description = "Message"

#--- for receipt upload
