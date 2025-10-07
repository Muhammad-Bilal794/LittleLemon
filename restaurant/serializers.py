from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Menu , Booking
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'