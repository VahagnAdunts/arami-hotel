from django.db import models

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('budget', 'Budget Room'),
        ('superior', 'Superior Room'),
    ]

    type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='budget')
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    total_count = models.PositiveIntegerField(default=1)  # total rooms of this type

    def __str__(self):
        return f"{self.get_type_display()}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f"Image for {self.room.get_type_display()}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.room.get_type_display()}"


class ContactMessage(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

class SeasonalPrice(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='seasonal_prices')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.room.get_type_display()} ({self.start_date} to {self.end_date}) – {self.price_per_night} AMD"


