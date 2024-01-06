from django.contrib import admin

# Register your models here.
from .models import Menu, Booking

# from .models import Rating, Category, MenuItem, Cart, Order, OrderItem

admin.site.register(Menu)
admin.site.register(Booking)

# admin.site.register(Rating)
# admin.site.register(Category)
# admin.site.register(MenuItem)
# admin.site.register(Cart)
# admin.site.register(Order)
# admin.site.register(OrderItem)