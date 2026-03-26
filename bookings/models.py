from django.db import models
from django.core.exceptions import ValidationError

class RoomCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    class Meta:
        verbose_name = "Категорія кімнати/місця"
        verbose_name_plural = "Категорії кімнат/місць"

    def __str__(self):
        return self.name
    
class Room(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, null=True, related_name='rooms', verbose_name="Категорія")
    
    name = models.CharField(max_length=100, verbose_name="Назва кімнати/місця")
    capacity = models.PositiveIntegerField(verbose_name="Вмістимість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    features = models.TextField(blank=True, verbose_name="Особливості (через кому)")
    
    class Meta:
        verbose_name = "Кімната"
        verbose_name_plural = "Кімнати"

    def __str__(self):
        category_name = self.category.name if self.category else "Без категорії"
        return f"{self.name} ({category_name})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', verbose_name="Кімната")
    user_name = models.CharField(max_length=150, verbose_name="Ім'я користувача")
    user_email = models.EmailField(verbose_name="Email")
    start_time = models.DateTimeField(verbose_name="Час початку")
    end_time = models.DateTimeField(verbose_name="Час завершення")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Час завершення має бути пізніше часу початку.")

    def __str__(self):
        return f"Бронювання: {self.user_name} -> {self.room.name} ({self.start_time.strftime('%d.%m.%Y')})"