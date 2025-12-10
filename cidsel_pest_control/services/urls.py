# services/urls.py
from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView

from services.views import get_notification_detail


urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    #------------- for CUSTOMER TEMPLATE -----------------
    #this is for CUSTOMER SIGNUP AND LOGIN
    path('signup/', views.signup, name='customer_signup'), 
    path('login/', views.user_login, name='login'),

    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # this is for book appointment button in dashboard.html
    path('book-appointment/', views.book_appointment, name='book_appointment'), 
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    path('recent-appointment/', views.recent_appointment, name='recent_appointment'),
    
    
    path('appointments/', views.admin_appointment_view, name='admin_appointment_view'),
    # path('appointments/<int:appointment_id>/done/', views.mark_done, name='mark_done'),
    # path('mark-done-ajax/<int:appointment_id>/', views.mark_done_ajax, name='mark_done_ajax'),
    path('update-appointment-status/<int:appointment_id>/', views.update_appointment_status, name="update_appointment_status"),
    path("get-progress-steps/", views.get_progress_steps, name="get_progress_steps"),
    path("get-progress-photos/", views.get_progress_photos, name="get_progress_photos"),
    
    
    path('admin-panel/appointment/', views.appointment, name='appointment'),
    
    #--- for CUSTOMERS 
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('services/', views.services, name='services'),
    
    path('faqs/', views.faqs, name='faqs'),
    
    path('feedback/', views.feedback, name='feedback'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("upload-receipt/<int:appointment_id>/", views.upload_receipt, name="upload_receipt"),
    path('receipt/delete/<int:receipt_id>/', views.delete_receipt, name='delete_receipt'),


    #------------- for ADMIN TEMPLATE -----------------
    # this is a for Admin LOGIN and SIGNUP
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-signup/', views.admin_signup_view, name='admin_signup'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    #--- for admin Home page
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_home'),
    
    path("send-message/", views.send_message, name="send_message"),
    path("load-messages/", views.load_messages, name="load_messages"),
    path("admin-send-message/", views.admin_send_message, name="admin_send_message"),
    
    #--- for upload and deleting image 
    path("upload/", views.upload_photo, name="upload"),
    path("delete-picture/<int:photo_id>/", views.delete_picture, name="delete_picture"),
    
    
    path('admin-panel/analytics/', views.analytics, name='analytics'),
    
    
    path('admin-panel/pest-activity/', views.pest_activity, name='pest_activity'),
    
    path('admin/pest-activity/', views.pest_activity_view, name='pest_activity'),
    path('admin/pest-activity-data/', views.pest_activity_data, name='pest_activity_data'),


    path('admin-panel/customers/', views.customers, name='customers'),
    path('customers-review/', views.customers_review, name='customers_review'),
    path("get-customer-detail/<int:pk>/", views.get_customer_detail, name="get_customer_detail"),
    #path('admin-panel/customers_review/', views.customers_review, name='customers_review'),


    path('admin-panel/inventory/', views.inventory, name='inventory'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('inventory/edit/<int:pk>/', views.product_update, name='product_update'),
    path('inventory/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path("get-recommended-items/", views.get_recommended_items, name="get_recommended_items"),

    
    path('admin-panel/sales.html/', views.sales, name='sales'),
    
    path('admin-panel/report.html/', views.reports, name='reports'),
    path('export-sales-report/', views.export_sales_report, name='export_sales_report'),
    path("sales-report/", views.sales_report, name="sales_report"),
    path("sales-by-month/", views.sales_by_month, name="sales_by_month"),
    
    path('logout/', views.logout_view, name='logout'),
    
    
    
    #------- this is for TECHNICIAN signup and login --------
    path('technician/login/', views.technician_login, name='technician_login'),
    path('technician/signup/', views.technician_signup, name='technician_signup'),
    path('technician/dashboard/', views.technician_dashboard, name='technician_dashboard'),
    #--- for content
    path('home-page/', views.home_page, name='home_page'),
    path('update-tech-status/', views.update_technician_status, name="update_tech_status"),


    #--- for notification
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_notification_read, name='mark_notification_read'),
    #path('technician/notifications/', views.technician_notifications, name='technician_notifications'),

    #---- for single modal notification in admin
    path('get-notification-detail/', get_notification_detail, name='get_notification_detail'),

    
    #--- for photo documentation
    path('photo-documentation/', views.photo_documentation, name='photo_documentation'),
    path('photo-documentation/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    
    #--- for verification
    path('verification-route/', views.verification_route, name='verification_route'),
    path('verification-route/<int:appointment_id>/', views.verification_route, name='verification_route'),
    path('assign-verification/', views.assign_verification_ajax, name='assign_verification_ajax'),
    path('get-technicians/', views.get_technicians, name='get_technicians'),
    
    path("technician/accept/", views.technician_accept_job, name="technician_accept_job"),
    path('upload-progress-photo/', views.upload_progress_photo, name='upload_progress_photo'),


    path("update-verification-status/", views.update_verification_status, name="update_verification_status"),
    path('dismiss_notification/', views.dismiss_notification, name='dismiss_notification'),
    
]


