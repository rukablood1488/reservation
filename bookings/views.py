import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Room, RoomCategory, Booking
from .forms import BookingForm, RegisterForm, RoomListingForm


def room_list(request):
    category_id = request.GET.get('category')
    categories  = RoomCategory.objects.all()
    rooms = Room.objects.filter(is_active=True)
    if category_id:
        rooms = rooms.filter(category_id=category_id)
    return render(request, 'bookings/room_list.html', {
        'rooms':             rooms,
        'categories':        categories,
        'selected_category': category_id,
    })


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_active=True)
    return render(request, 'bookings/room_detail.html', {'room': room})


def calendar_view(request):
    rooms    = Room.objects.filter(is_active=True)
    bookings = Booking.objects.filter(
        status__in=['confirmed', 'pending']
    ).select_related('room')

    room_id = request.GET.get('room')
    if room_id:
        bookings = bookings.filter(room_id=room_id)

    color_map = {
        'confirmed': '#34d399',
        'pending':   '#fbbf24',
        'cancelled': '#f87171',
    }

    events = []
    for b in bookings:
        events.append({
            'id':             b.id,
            'title':          b.room.name,
            'start':          b.start_time.isoformat(),
            'end':            b.end_time.isoformat(),
            'color':          color_map.get(b.status, '#8b5cf6'),
            'roomId':         b.room.id,
            'extendedProps': {
                'guest':          b.user_name,
                'status_display': b.get_status_display(),
            },
        })

    return render(request, 'bookings/calendar.html', {
        'rooms':                rooms,
        'calendar_events_json': json.dumps(events),
    })


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking      = form.save(commit=False)
            booking.user = request.user 
            booking.save()

            confirm_url = request.build_absolute_uri(
                f'/booking/confirm/{booking.confirmation_token}/'
            )
            subject = f'Підтвердіть бронювання: {room.name}'
            message = (
                f'Вітаємо, {booking.user_name}!\n\n'
                f'Ви забронювали "{room.name}":\n'
                f'  Початок: {booking.start_time.strftime("%d.%m.%Y %H:%M")}\n'
                f'  Кінець:  {booking.end_time.strftime("%d.%m.%Y %H:%M")}\n\n'
                f'Щоб ПІДТВЕРДИТИ бронювання, перейдіть за посиланням:\n{confirm_url}\n\n'
                f'Якщо ви не робили цього запиту — просто ігноруйте цей лист.\n'
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.user_email])
            except Exception as e:
                print(f"Помилка відправки пошти: {e}")

            return render(request, 'bookings/success.html', {'booking': booking})
    else:
        initial = {
            'room':       room,
            'user_name':  request.user.get_full_name() or request.user.username,
            'user_email': request.user.email,
        }
        form = BookingForm(initial=initial)

    return render(request, 'bookings/booking_form.html', {'form': form, 'room': room})


def confirm_booking(request, token):
    booking = get_object_or_404(Booking, confirmation_token=token)

    if booking.status == 'confirmed':
        already_confirmed = True
    elif booking.status == 'cancelled':
        return render(request, 'bookings/confirm_booking.html', {
            'booking': booking,
            'error':   'Це бронювання вже скасовано і не може бути підтверджено.',
        })
    else:
        booking.status = 'confirmed'
        booking.save()
        already_confirmed = False

    return render(request, 'bookings/confirm_booking.html', {
        'booking':           booking,
        'already_confirmed': already_confirmed,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    total     = bookings.count()
    confirmed = bookings.filter(status='confirmed').count()
    pending   = bookings.filter(status='pending').count()

    return render(request, 'bookings/my_bookings.html', {
        'bookings':  bookings,
        'total':     total,
        'confirmed': confirmed,
        'pending':   pending,
    })


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = RoomListingForm(request.POST)
        if form.is_valid():
            room = form.save(owner=request.user)
            messages.success(request, f'Оселю "{room.name}" успішно додано!')
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomListingForm()

    return render(request, 'bookings/create_listing.html', {'form': form})


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


def login_view(request):
    if request.user.is_authenticated:
        return redirect('room_list')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect(request.POST.get('next') or 'room_list')
        else:
            error = 'Невірний логін або пароль.'
    return render(request, 'bookings/login.html', {
        'error': error,
        'next':  request.GET.get('next', ''),
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('room_list')
