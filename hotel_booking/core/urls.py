from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:room_type>/', views.room_detail, name='room_detail'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('availability/', views.check_availability, name='check_availability'),
    path('contact-submit/', views.contact_submit, name='contact_submit'),
    path('rooms/', views.rooms, name='rooms'),
]