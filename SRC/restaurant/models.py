from django.db import models
from django.forms.fields import ChoiceField
from django.core.validators import MinValueValidator

from accounts.models import RestaurantManager
import jdatetime

class Address(models.Model):
    city = models.CharField(max_length=60,blank=True,null=True)
    street = models.CharField(max_length=60,blank=True,null=True)
    plaque = models.IntegerField(validators=[MinValueValidator(1)],blank=True,null=True)
    #customer_id = models.ManyToManyField("accounts.Customer", through = 'AddressUser')
    customer_id = models.ForeignKey("accounts.Customer",on_delete=models.CASCADE)

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.city+"_"+self.street

    def save(self, *args, **kwargs):
            primary_address = Address.objects.filter(is_primary=True,customer_id = self.customer_id)

            if self.is_primary:
                if primary_address:
                    primary_address.update(is_primary = False)  
            
            else:
                if primary_address and primary_address.values_list('id')[0][0] != self.id:
                    pass
                else:
                    self.is_primary = True

            super(Address, self).save(*args, **kwargs)    
             

# class AddressUser(models.Model):
#     #address = models.ForeignKey(Address, on_delete = models.CASCADE,null = True, blank=True) 
#     customer = models.ForeignKey("accounts.Customer", on_delete = models.CASCADE)
#     def __str__(self):
#         if self.customer.email :
#             return self.customer.email 
#         else:
#             return "None"    

class Restaurnt(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField( max_length=50,unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        

    


class Meal(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Meal, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class Branch(models.Model):
    name = models.CharField(max_length=60)
    city =models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    description = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurnt, on_delete=models.CASCADE, related_name = "restuarant_branch" )
    manager_restaurant = models.OneToOneField("accounts.RestaurantManager",on_delete=models.CASCADE,related_name = "manager_branch" )
    branch_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name = "category_branch" )
    is_primary = models.BooleanField(default=False)
    def __str__(self):
        return self.name

          
    def save(self, *args, **kwargs):
            primary_branch = Branch.objects.filter(is_primary=True,restaurant = self.restaurant)

            if self.is_primary:
                if primary_branch:
                    primary_branch.update(is_primary = False)  
            
            else:
                if primary_branch and primary_branch.values_list('id')[0][0] != self.id:
                    pass
                else:
                    self.is_primary = True

            super(Branch, self).save(*args, **kwargs)  
    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.created)    

     

class Food(models.Model):
    name = models.CharField(max_length=60)
    food_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name = "category_food")
    meal_category = models.ManyToManyField(Meal,related_name = "meal_food" )
    description = models.CharField( max_length=300,null=True,blank =True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name

    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.created)    


class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE,related_name = "food_menu" )
    
    def __str__(self):
        return self.branch.name +"_"+self.food.name

class OrderStatus(models.Model):
    status = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.status


class Order(models.Model): 
    customer = models.ForeignKey("accounts.Customer", on_delete=models.CASCADE,related_name = "customer_order")
    created = models.DateTimeField(auto_now_add=True)
    status_id = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='status_order')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        if self.customer.email:
            return self.customer.email +"_"+self.status_id.status
        else: 
            return self.status_id.status 
    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.created)   

    @property
    def get_cart_total(self):
        orderitems = OrderItem.objects.filter(order_id=self.id)
        if orderitems:
            return sum([item.get_total_price for item in orderitems]) 
        else:
            return 0          
   

class OrderItem(models.Model):
    quantity = models.IntegerField()
    menu_id = models.ForeignKey(Menu,on_delete=models.CASCADE, related_name="menu_order_item")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    def __str__(self) :
        if self.order_id.customer.email: 
            return self.menu_id.food.name +"_"+ self.order_id.customer.email +"_"+str(self.quantity)
        else: 
            return self.menu_id.food.name +"_"+str(self.quantity)  

    @property
    def get_total_price(self):
        menu_price = Menu.objects.filter(id=self.menu_id.id).values_list("price")[0][0]
        print("pppppppppppp",menu_price)
        return menu_price * self.quantity  
               
          
   
   
    
