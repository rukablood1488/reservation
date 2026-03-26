from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.create_booking, name='create_booking'),
]