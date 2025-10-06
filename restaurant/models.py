from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Booking(models.Model) :
    name=models.CharField(max_length=255)
    no_of_guests=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(6)])
    BookingDate=models.DateTimeField()
    def __str__(self):
        return f"name: {self.name}, no of guests: {self.no_of_guests}, Booking date: {self.BookingDate}"
        
class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99999)
        ]
    )

    def __str__(self):
        return self.title
    