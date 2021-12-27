from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Address)
admin.site.register(Restaurnt)
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Branch)
admin.site.register(OrderStatus)

