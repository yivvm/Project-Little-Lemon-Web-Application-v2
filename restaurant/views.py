from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Menu, Booking, Category, MenuItem
from .forms import BookingForm

from .serializers import (
    MenuSerializer,
    BookingSerializer,
    CategorySerializer,
    MenuItemSerializer,
)


class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


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

