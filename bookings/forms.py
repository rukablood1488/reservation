from django import forms
from .models import Booking, Room, Location, RoomCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['room', 'user_name', 'user_email', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room       = cleaned_data.get('room')
        start_time = cleaned_data.get('start_time')
        end_time   = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Час завершення має бути пізніше часу початку.")

        if room and start_time and end_time:
            overlapping = Booking.objects.filter(
                room=room,
                status='confirmed',
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            if overlapping.exists():
                raise forms.ValidationError("Ця кімната вже заброньована на обраний період.")

        return cleaned_data


class RoomListingForm(forms.Form):
    """Form for regular users to create/propose a room listing."""
    name     = forms.CharField(max_length=100, label="Назва оселі",
                               widget=forms.TextInput(attrs={'placeholder': 'Затишна студія в центрі'}))
    category = forms.ModelChoiceField(queryset=RoomCategory.objects.all(),
                                      label="Категорія", empty_label="— Оберіть категорію —")
    capacity = forms.IntegerField(min_value=1, label="Місткість (осіб)",
                                  widget=forms.NumberInput(attrs={'placeholder': '2'}))
    price    = forms.DecimalField(max_digits=10, decimal_places=2, label="Ціна за ніч (₴)",
                                  widget=forms.NumberInput(attrs={'placeholder': '500'}))
    country  = forms.CharField(max_length=100, label="Країна",
                               widget=forms.TextInput(attrs={'placeholder': 'Україна'}),
                               initial='Україна')
    city     = forms.CharField(max_length=100, label="Місто",
                               widget=forms.TextInput(attrs={'placeholder': 'Київ'}))
    address  = forms.CharField(max_length=255, label="Адреса", required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'вул. Хрещатик, 1'}))
    features = forms.CharField(max_length=500, label="Особливості", required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'WiFi Парковка Басейн'}))

    def save(self, owner):
        """Create Location + Room and return the Room instance."""
        data = self.cleaned_data
        location, _ = Location.objects.get_or_create(
            country=data['country'],
            city=data['city'],
            address=data.get('address', ''),
        )
        room = Room.objects.create(
            owner=owner,
            category=data['category'],
            location=location,
            name=data['name'],
            capacity=data['capacity'],
            price=data['price'],
            features=data.get('features', ''),
            is_active=True,
        )
        return room
