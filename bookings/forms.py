from django import forms
from .models import Booking, Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'user_name', 'user_email', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if room and start_time and end_time:
            # Логіка перевірки накладання дат:
            overlapping_bookings = Booking.objects.filter(
                room=room,
                status='confirmed',
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if overlapping_bookings.exists():
                raise forms.ValidationError("Ця кімната вже заброньована на обраний період.")
        return cleaned_data