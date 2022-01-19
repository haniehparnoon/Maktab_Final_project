from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(null = True, blank = True)
    device = models.CharField(max_length=50, null = True, blank = True)
    role_choices = [
        ("Admin","Admin"),
        ("Manager","Manager"),
        ("Customer","Customer"),
    ] 
    role = models.CharField(choices= role_choices,default="Customer", max_length=9)
    
class Admin(CustomUser):
    class Meta:
        proxy = True

    
    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = True
        super(Admin, self).save(*args, **kwargs)    

          
class RestaurantManager(CustomUser):
  
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = False
            self.is_staff = True
        super(RestaurantManager, self).save(*args, **kwargs)    

class Customer(CustomUser):

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id :
            self.is_superuser = False
            self.is_staff = False
        super(Customer, self).save(*args, **kwargs)    

