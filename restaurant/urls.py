from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 

    # path('menu', views.MenuView.as_view()),
    path('booking', views.BookingView.as_view()),

    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.CategoriesView.as_view()),

    # path('ratings', views.RatingsView.as_view()),
    # path('cart/menu-items', views.CartView.as_view()),
    # path('orders', views.OrdersView.as_view()),
    # path('orders/<int:pk>', views.SingleOrderView.as_view()),
    # path(
    #     'groups/manager/users', 
    #     views.GroupViewSet.as_view(
    #         {'get': 'list', 'post': 'create', 'delete': 'destroy'}
    #     )
    # ),
    # path(
    #     'groups/delivery-crew/users',
    #     views.DeliveryCrewViewSet.as_view(
    #         {'get': 'list', 'post': 'create', 'delete': 'destroy'}
    #     )
    # ),
]
