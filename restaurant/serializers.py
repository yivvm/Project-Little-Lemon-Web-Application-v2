
from rest_framework import serializers 
from decimal import Decimal
from django.contrib.auth.models import User 


from .models import Menu, Booking, Category, MenuItem

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer): 
    category = serializers.PrimaryKeyRelatedField(
        queryset = MenuItem.objects.all(), 
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

