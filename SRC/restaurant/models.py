from django.db import models
from django.forms.fields import ChoiceField
from django.core.validators import MinValueValidator

from accounts.models import RestaurantManager
#from jdatetime

class Address(models.Model):
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    plaque = models.IntegerField(validators=[MinValueValidator(1)])
    customer_id = models.ManyToManyField("accounts.Customer", through = 'AddressUser')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.city+"_"+self.street

    def save(self, *args, **kwargs):
        if self.is_primary:
            try:
                temp = Address.objects.get(is_primary=True)
                if self != temp:
                    self.is_primary = False
                    self.save()
            except Address.DoesNotExist:
                pass
        super(Address, self).save(*args, **kwargs)
             

class AddressUser(models.Model):
    address = models.ForeignKey(Address, on_delete = models.SET_NULL,null = True, blank=True) 
    customer = models.ForeignKey("accounts.Customer", on_delete = models.CASCADE, null = True, blank=True)
    def __str__(self):
        if self.customer.email :
            return self.customer.email 
        else:
            return "None"    

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
        return super(Category, self).save(*args, **kwargs)
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
        if self.is_primary:
            try:
                temp = Branch.objects.get(is_primary=True)
                if self != temp:
                    self.is_primary = False
                    self.save()
            except Branch.DoesNotExist:
                pass
        super(Branch, self).save(*args, **kwargs)

    # @property 
    # def created_at_jalali(self):
    #     return jdatetime.datetime.fromgregorian(datetime= self.order_date)     

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
        return self.branch.name +"_"+self.food.name

class OrderStatus(models.Model):
    status = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.status


class Order(models.Model): 
    customer_id = models.ForeignKey(AddressUser, on_delete=models.CASCADE,related_name = "customer_order")
    created = models.DateTimeField(auto_now_add=True)
    status_id = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='status_order')
    def __str__(self):
        if self.customer_id.customer.email:
            return self.customer_id.customer.email +"_"+self.status_id.status
        else: 
            return self.status_id.status   
   

class OrderItem(models.Model):
    quantity = models.IntegerField()
    menu_id = models.ForeignKey(Menu,on_delete=models.CASCADE, related_name="menu_order_item")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    def __str__(self) :
        if self.order_id.customer_id.customer.email: 
            return self.menu_id.food.name +"_"+ self.order_id.customer_id.customer.email +"_"+str(self.quantity)
        else: 
            return self.menu_id.food.name +"_"+str(self.quantity)   
   
   
    
