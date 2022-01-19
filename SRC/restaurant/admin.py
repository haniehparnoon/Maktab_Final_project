from django.contrib import admin
from .models import *
from accounts.models import *


# Register your models here.
#admin.site.register(Address)
class BranchInline(admin.TabularInline):
    model = Branch  

class FoodInline(admin.TabularInline):
    model = Food 

class FoodMealInline(admin.TabularInline):
    model = Food.meal_category.through


@admin.register(Address)
class CustomAddress(admin.ModelAdmin): 
    model = Address
    list_display = ['id','city','street','plaque','is_primary','customer_id']
    list_editable = ['city','street','plaque','is_primary',]
    empty_value_display = 'empty'
    list_filter = ['city']
    search_fields = ('city','street')
    list_per_page = 5
   
    fieldsets = (
        (None, {
            "fields": (
                'city','street','plaque','is_primary',
            ),
           
        }),
        ("fk fields",{
              "fields": ('customer_id',
                
            ),
            
        }),
    )


@admin.register(Restaurnt)
class CustomRestaurnt(admin.ModelAdmin): 
    model = Restaurnt
    list_display = ['id','name',]
    list_editable = ['name',]
    empty_value_display = 'empty'
    list_filter = ['name']
    search_fields = ('name',)
    list_per_page = 5
    inlines = [BranchInline]
   
   

@admin.register(Category)
class CustomCategory(admin.ModelAdmin): 
    model = Category
    list_display = ['id','name',]
    list_editable = ['name',]
    empty_value_display = 'empty'
    list_filter = ['name']
    search_fields = ('name',)
    list_per_page = 5
    inlines = [BranchInline,FoodInline]


@admin.register(Meal)
class CustomMeal(admin.ModelAdmin): 
    model = Meal
    list_display = ['id','name',]
    list_editable = ['name',]
    empty_value_display = 'empty'
    list_filter = ['name']
    search_fields = ('name',)
    list_per_page = 5
    inlines = [FoodMealInline]



@admin.register(Food)
class CustomFood(admin.ModelAdmin): 
    model = Food
    list_display = ['id','name','description',]
    list_editable = ['name','description',]
    empty_value_display = 'empty'
    list_filter = ['name','food_category','meal_category']
    search_fields = ('name',)
    list_per_page = 5
    
    



@admin.register(Menu)
class CustomMenu(admin.ModelAdmin): 
    model = Menu
    list_display = ['id','food','price','quantity',]
    list_editable = ['food','price','quantity',]
    empty_value_display = 'empty'
    list_per_page = 5
     
    fieldsets = (
        (None, {
            "fields": (
                'price','quantity',
            ),
           
        }),
        ("fk fields",{
              "fields": ('branch','food',
                
            ),
            
        }),
    )



@admin.register(Order)
class CustomOrder(admin.ModelAdmin): 
    model = Order
    list_display = ['id','customer','status_id','address',]
    list_editable = ['customer','status_id','address',]
    empty_value_display = 'empty'
    list_per_page = 5
     
    



@admin.register(OrderItem)
class CustomOrderItem(admin.ModelAdmin): 
    model = OrderItem
    list_display = ['id','quantity','menu_id','order_id',]
    list_editable = ['quantity','menu_id','order_id']
    empty_value_display = 'empty'
    list_per_page = 5


@admin.register(Branch)
class CustomBranch(admin.ModelAdmin): 
    model = Branch
    list_display = ['id','name','city','address','description','restaurant','manager_restaurant','branch_category','is_primary']
    list_editable = ['name','city','address','description','restaurant','manager_restaurant','branch_category','is_primary']
    empty_value_display = 'empty'
    list_per_page = 5
    search_fields = ('name',)
    fieldsets = (
        (None, {
            "fields": (
                'name','city','address','description','is_primary',
            ),
           
        }),
        ("fk fields",{
              "fields": ('restaurant','manager_restaurant','branch_category',
                
            ),
            
        }),
    )


@admin.register(OrderStatus)
class CustomOrderStatus(admin.ModelAdmin): 
    model = OrderStatus
    list_display = ['id','status']
    list_editable = ['status',]
    empty_value_display = 'empty'
    list_per_page = 5




