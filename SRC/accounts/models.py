from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    device = models.CharField(max_length=50, null = True, blank = True) 
    
class Admin(CustomUser):
    class Meta:
        proxy = True
          
class RestaurantManager(CustomUser):
    class Meta:
        proxy = True

class Customer(CustomUser):
    class Meta:
        proxy = True

