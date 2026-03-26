from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Room, RoomCategory, Booking
from .forms import BookingForm

def room_list(request):
    category_id = request.GET.get('category')
    categories = RoomCategory.objects.all()
    if category_id:
        rooms = Room.objects.filter(category_id=category_id)
    else:
        rooms = Room.objects.all()
    return render(request, 'bookings/room_list.html', {
        'rooms': rooms, 
        'categories': categories
    })

def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Відправка підтвердження на Email
            subject = f'Підтвердження бронювання: {room.name}'
            message = f'Вітаємо, {booking.user_name}!\nВаше бронювання на {booking.start_time} прийнято в обробку.'
            recipient_list = [booking.user_email]
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            except Exception as e:
                print(f"Помилка відправки пошти: {e}")

            return render(request, 'bookings/success.html', {'booking': booking})
    else:
        form = BookingForm(initial={'room': room})
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'room': room})