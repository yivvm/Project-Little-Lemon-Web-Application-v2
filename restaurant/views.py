from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Menu, Booking, Category, MenuItem
from .forms import BookingForm

# from .models import Rating, Cart, Order, OrderItem

from .serializers import (
    MenuSerializer,
    BookingSerializer,
    # RatingSerializer,
    CategorySerializer,
    MenuItemSerializer,
    # CartSerializer,
    # OrderSerializer,
    UserSerializer,
)


# class BookingViewSet(viewsets.ModelViewSet):
class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [permissions.IsAuthenticated]


class MenuView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ["category__title"]
    ordering_field = ["price", "inventory"]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]


@api_view()
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def msg(request):
    return Response({"message" : "This view is protected"})


# Create views of webpages
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = (
            Booking.objects.filter(reservation_date=data['reservation_date'])
            .filter(reservation_slot=data['reservation_slot'])
            .exists()
        )
        if exist == False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=date['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
        
        date = request.GET.get('date', datetime.today().date())
        
        bookings = Booking.objects.all().filter(reservation_date=date)
        booking_json = serializers.serialize('json', bookings)

        return HttpResponse(booking_json, content_type='application/json')



# class RatingsView(generics.ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return []
        
#         return [IsAuthenticated()]


# class CartView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Cart.objects.all().filter(user=self.request.user)
    
#     def delete(self, request, *args, **kwargs):
#         Cart.objects.all().filter(user=self.request.user).delete()
#         return Response('OK')


# class OrdersView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # admin = superuser
#         if self.request.user.is_superuser:
#             return Order.objects.all()
#         # customer = no group
#         elif self.request.user.groups.count() == 0:  
#             return Order.objects.all().filter(user=self.request.user)
#         # delivery crew
#         elif self.request.user.groups.filter(name='Delivery Crew').exists():  
#             return Order.objects.all().filter(delivery_crew=self.request.user)  # only show orders assigned to this deliveryman
#         # delivery crew or manager
#         else:
#             return Order.objects.all()
    
#     def create(self, request, *args, **kwargs):
#         menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
#         if menuitem_count == 0:
#             return Response({'message:': 'No item in cart'})
        
#         data = request.data.copy()
#         total = self.get_total_price(self.request.user)
#         data['total'] = total
#         data['user'] = self.request.user.id

#         order_serializer = OrderSerializer(data=data)
#         if order_serializer.is_valid():
#             order = order_serializer.save()

#             items = Cart.objects.all().filter(user=self.request.user).all()

#             for item in items.values():
#                 orderitem = OrderItem(
#                     order=order,
#                     menuitem_id=item['menuitem_id'],
#                     price=item['price'],
#                     quantity=item['quantity'],
#                 )
#                 orderitem.save()
            
#             Cart.objects.all().filter(user=self.request.user).delete()  # delete cart items

#             result = order_serializer.data.copy()
#             result['total'] = total
#             return Response(order_serializer.data)
    
#     def get_total_price(self, user):
#         total = 0
#         items = Cart.objects.all().filter(user=user).all()
#         for item in items.values():
#             total += item['price']
#         return total


# class SingleOrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         # customer = no group
#         if self.request.user.groups.count == 0:
#             return Response('Not OK')
#         else:
#             return super().update(request, *args, **kwargs)


# class GroupViewSet(viewsets.ViewSet):
#     permission_classes = [IsAdminUser]

#     def list(self, request):
#         users = User.objects.all().filter(groups__name='Manager')
#         items = UserSerializer(users, many=True)
#         return Response(items.data)
    
#     def create(self, request):
#         user = get_object_or_404(User, username=request.data['username'])
#         managers = Group.objects.get(name='Manager')
#         managers.user_set.add(user)
#         return Response({'message:': 'User added to the manager group'}, 200) 
    
#     def destroy(self, request):
#         user = get_object_or_404(User, username=request.data['username'])
#         managers = Group.objects.get(name='Manager')
#         managers.user_set.remove(user)
#         return Response({'message:': 'User removed from the manager group'}, 200) 


# class DeliveryCrewViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         users = User.objects.all().filter(groups__name='Delivery Crew')
#         items = UserSerializer(users, many=True)
#         return Response(items.data)
    
#     def create(self, request):
#         # only for superuser/admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({'message:': 'forbidden'}, status.HTTP_403_FORBIDDEN) 
    
#         user = get_object_or_404(User, username=request.data['username'])
#         dc = Group.objects.get(name='Delivery Crew')
#         dc.user_set.add(user)
#         return Response({'message:': 'User added to the delivery crew group'}, 200) 
    
#     def destroy(self, request):
#         # only for superuser/admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({'message:': 'forbidden'}, status.HTTP_403_FORBIDDEN) 
            
#         user = get_object_or_404(User, username=request.data['username'])
#         managers = Group.objects.get(name='Delivery Crew')
#         managers.user_set.remove(user)
#         return Response({'message:': 'User removed from the delivery crew group'}, 200) 