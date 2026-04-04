from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.create_booking, name='create_booking'),
    path('booking/confirm/<uuid:token>/', views.confirm_booking, name='confirm_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
