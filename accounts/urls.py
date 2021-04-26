from os import name
from django.urls import path
from . import views
import accounts

app_name = 'accounts'
urlpatterns = [
    path('',views.home, name="home"),
    path('user/',views.userPage, name="user"),
    path('user_settings/',views.accountSettings,name='user_settings'),


    path('register/',views.register, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),

    path('products/',views.products,name="products"),
    path('customers/<str:pk>/',views.customers, name="customers"),

    path('create_order/<str:pk>',views.createOrder,name="create_order"),
    path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order"),
]