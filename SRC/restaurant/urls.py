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
    path("cart/orderitem_delete/<int:pk>/",OrderItemDelete.as_view(),name = "orderitem_delete"),
    path("cart/orderitem_edit/<int:pk>/",OrderItemEdit.as_view(),name = "orderitem_edit"),
   # path('db_temp/', sample_django_template, name="json_db_temp"),
   path("signup_base/",SignupBase.as_view(), name = "signup_base"),
   path("signup_admin/",signup_admin,name = "signup_admin"),
   path("signup_manager/",signup_mamager,name = "signup_manager"),
   path("signup_customer/",signup_customer,name = "signup_customer"),
   path("customerhome/show_address/<int:pk>",ShowAddress.as_view(),name="show_address"),
   path("delete_address/<int:pk>/",DeleteAddress.as_view(),name = "delete_address"),
   path("edit_address/<int:pk>/",EditAddress.as_view(),name = "edit_address"),
   path("padd_address/<int:pk>/",padd_address,name = "padd_address"),
   path("ordered_history/<int:pk>",ordered_history, name = "ordered_history"),
   path("show_order_item/<int:pk>",show_order_item, name = "show_order_item"),
   path("adminhome/show_branch/<int:pk>",ShowBranch.as_view(),name="show_branch"),
   path("edit_branch/<int:pk>/",EditBranch.as_view(),name = "edit_branch"),
   path("menu_branch_item/<int:pk>/",MenuBranchItem.as_view(),name = "menu_branch_item"),
   path("menu_branch_item/menu_branch_item_createview/<int:pk>",MenuBranchItemCreateView.as_view(),name = "menu_branch_item_createview"),
   path("menu_branch_item/menu_item_edit/<int:pk>",MenuItemEdit.as_view(),name = "menu_item_edit"),
   path("menu_branch_item/menu_item_delete/<int:pk>",MenuItemDelete.as_view(),name = "menu_item_delete"),
   path("orders_list/<int:pk>",OrdersList.as_view(),name = "orders_list"),
   path("edit_order/<int:pk>",EditOrder.as_view(),name = "edit_order"),
   path("MenuItemBaseOnFood/<int:pk>",MenuItemBaseOnFood.as_view(),name='menu_item_base_on_Food'),
   

   
   

   
   

    
]