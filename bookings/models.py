import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Location(models.Model):
    country = models.CharField(max_length=100, verbose_name="Країна")
    city = models.CharField(max_length=100, verbose_name="Місто")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адреса")

    class Meta:
        verbose_name = "Локація"
        verbose_name_plural = "Локації"
        unique_together = ('country', 'city', 'address')

    def __str__(self):
        parts = [self.city, self.country]
        if self.address:
            parts.insert(0, self.address)
        return ", ".join(parts)


class RoomCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    class Meta:
        verbose_name = "Категорія кімнати/місця"
        verbose_name_plural = "Категорії кімнат/місць"

    def __str__(self):
        return self.name

    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class CategoryImage(models.Model):
    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE,
        related_name='images', verbose_name="Категорія"
    )
    image = models.ImageField(upload_to='categories/', verbose_name="Фото")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Підпис")
    is_main = models.BooleanField(default=False, verbose_name="Головне фото")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото категорії"
        verbose_name_plural = "Фото категорій"
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Фото для {self.category.name} {'(головне)' if self.is_main else ''}"

    def save(self, *args, **kwargs):
        if self.is_main:
            CategoryImage.objects.filter(
                category=self.category, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class Room(models.Model):
    category = models.ForeignKey(
        RoomCategory, on_delete=models.SET_NULL, null=True,
        related_name='rooms', verbose_name="Категорія"
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rooms', verbose_name="Локація"
    )
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

    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE,
        related_name='images', verbose_name="Кімната"
    )
    image = models.ImageField(upload_to='rooms/', verbose_name="Фото")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Підпис")
    is_main = models.BooleanField(default=False, verbose_name="Головне фото")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото кімнати"
        verbose_name_plural = "Фото кімнат"
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Фото для {self.room.name} {'(головне)' if self.is_main else ''}"

    def save(self, *args, **kwargs):
        if self.is_main:
            RoomImage.objects.filter(
                room=self.room, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


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
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Час завершення має бути пізніше часу початку.")

    def __str__(self):
        return f"Бронювання: {self.user_name} -> {self.room.name} ({self.start_time.strftime('%d.%m.%Y')})"
