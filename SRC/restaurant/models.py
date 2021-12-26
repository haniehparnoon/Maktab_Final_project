from django.db import models
from django.forms.fields import ChoiceField
from django.core.validators import MinValueValidator

from accounts.models import RestaurantManager


# inja ro to erd taghir bedam
class Address(models.Model):
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    plaque = models.IntegerField(validators=[MinValueValidator(1)])
    #
    customer_id = models.ManyToManyField("accounts.Customer", related_name="customer_address")
    #
    restaurant_manager_id = models.ForeignKey("accounts.RestaurantManager", on_delete=models.CASCADE,related_name="restaurant_address")
   

    def __str__(self):
        return self.city+"_"+self.street

class Restaurnt(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField( max_length=50)
    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class Branch(models.Model):
    # inja ham taghir bedam to erd
    name = models.CharField(max_length=60)
    # city =models.CharField(max_length=60)
    # street = models.CharField(max_length=60)
    description = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurnt, on_delete=models.CASCADE, related_name = "restuarant_branch" )
    manager_restaurant = models.ForeignKey("accounts.RestaurantManager",on_delete=models.CASCADE,related_name = "manager_branch" )
    #
    branch_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name = "category_branch" )
    
    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=60)
    food_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name = "category_food")
    meal_category = models.ManyToManyField(Meal,related_name = "meal_food" )
    description = models.CharField( max_length=300,null=True,blank =True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name


class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE,related_name = "food_menu" )
    
    def __str__(self):
        return self.food

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.status


class Order(models.Model): 
    customer_id = models.ForeignKey("accounts.Customer", on_delete=models.CASCADE,related_name = "customer_order")
    created = models.DateTimeField(auto_now_add=True)
    status_id = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='status_order')
    
    
    def __str__(self):
        return self.status

class OrderItem(models.Model):
    quantity = models.IntegerField()
    menu_id = models.ManyToManyField(Menu, related_name="menu_order_item")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.menu_id
   
    
