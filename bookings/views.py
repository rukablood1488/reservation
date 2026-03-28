from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Room, RoomCategory, Booking
from .forms import BookingForm, RegisterForm


def room_list(request):
    category_id = request.GET.get('category')
    categories = RoomCategory.objects.all()
    if category_id:
        rooms = Room.objects.filter(category_id=category_id)
    else:
        rooms = Room.objects.all()
    return render(request, 'bookings/room_list.html', {
        'rooms': rooms, 
        'categories': categories,
        'selected_category': category_id,
    })


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            subject = f'Підтвердження бронювання: {room.name}'
            message = (
                f'Вітаємо, {booking.user_name}!\n'
                f'Ваше бронювання на кімнату "{room.name}" '
                f'з {booking.start_time.strftime("%d.%m.%Y %H:%M")} '
                f'до {booking.end_time.strftime("%d.%m.%Y %H:%M")} прийнято в обробку.'
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.user_email])
            except Exception as e:
                print(f"Помилка відправки пошти: {e}")

            return render(request, 'bookings/success.html', {'booking': booking})
    else:
        initial = {
            'room': room,
            'user_name': request.user.get_full_name() or request.user.username,
            'user_email': request.user.email,
        }
        form = BookingForm(initial=initial)

    return render(request, 'bookings/booking_form.html', {'form': form, 'room': room})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user_email=request.user.email).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


def register(request):
    if request.user.is_authenticated:
        return redirect('room_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Ласкаво просимо.')
            return redirect('room_list')
    else:
        form = RegisterForm()
    return render(request, 'bookings/register.html', {'form': form})