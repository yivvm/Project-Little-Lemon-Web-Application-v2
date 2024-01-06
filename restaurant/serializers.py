
from rest_framework import serializers 
from decimal import Decimal
# from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User 

# from .models import Rating, Cart, Order, OrderItem 

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



# class RatingSerializer(serializers.ModelSerializer): 
#     user = serializers.PrimaryKeyRelatedField(
#     queryset=User.objects.all(), 
#     default=serializers.CurrentUserDefault()
#     )

#     class Meta:
#         model = Rating
#         fields = ['user', 'menuitem_id', 'rating']

#         validators = [
#             UniqueTogetherValidator(
#                 queryset = Rating.objects.all(), 
#                 fields=['user', 'menuitem_id']
#             )
#         ]

#         extra_kwargs = {
#             'rating': {'max_value' : 5, 'min_value' : 0}
#         }


# class CartSerializer(serializers.ModelSerializer): 
#     user = serializers.PrimaryKeyRelatedField(
#         queryset = Rating.objects.all(), 
#         default = serializers.CurrentUserDefault()
#     )

#     def validate(self, attributes):
#         attributes["price"] = attributes["quantity"] * attributes["unit_price"]
#         return attributes

#     class Meta:
#         model = Cart
#         fields = ['user', 'menuitem', 'unit_price', 'price', 'quantity']
#         extra_kwargs = {
#             'price': {'read_only' : True}
#         } 


# class OrderItemSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = OrderItem
#         fields = ['order', 'menuitem', 'quantity', 'price']


# class OrderSerializer(serializers.ModelSerializer): 
#     orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'orderitem']

