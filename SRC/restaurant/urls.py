from django.urls import path
from .views import *

urlpatterns = [
    #path('', HomePage.as_view(), name='home'),
    path('adminhome/', AdminHome.as_view(), name='home_admin'), 
    path('managerhome/', ManagerHome.as_view(), name='home_manager'), 
    path('customerhome/', CustomerHome.as_view(), name='home_customer'),
    path('adminhome/Foods/', FoodList.as_view(), name='Foods'),
    path('adminhome/categoryadd/', AddCategory.as_view(), name='category_add'),
    path('adminhome/Foods/editfood/<int:pk>/', EditFood.as_view(), name='food_edit'),
    path('adminhome/Foods/deletefood/<int:pk>/', DeleteFood.as_view(), name='food_delete'),
    path('',BranchList.as_view(), name = 'home'),
    path('menurestaurant/<int:pk>/',menuRestaurant.as_view(),name ="menurestaurant"),
    path('item/<int:pk>',menu_item,name="menu_item"),
    path('cart/', cart, name="cart"),

    
]