from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin): 
    model = CustomUser
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username',]
    empty_value_display = 'empty'
    list_filter = ['email']
    search_fields = ('username','email')
    list_per_page = 5
    fieldsets = (
        (None, {
            "fields": (
                'email','username','password','device',
            ),
           
        }),
        ("status",{
              "fields": (
                'is_superuser','is_staff','is_active'
            ),
            
        }),
    )
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()
    

@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    model = Admin
    list_display = ["id",'email','username']
    list_editable = ['username']
    empty_value_display = 'empty'
    list_display_links = ['email']
    list_filter = ['email']
    search_fields = ('username','email')
    list_per_page = 5
    fieldsets = (
        (None, {
            "fields": (
                'email','username','password','device',
                
            ),
        }),
    )
    

    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser = True)
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()    


@admin.register(RestaurantManager)
class CustomRestaurantManager(admin.ModelAdmin):
    model = Admin
    list_display = ["id",'email','username']
    list_editable = ['username']
    empty_value_display = 'empty'
    list_display_links = ['email']
    list_filter = ['email']
    search_fields = ('username','email')
    list_per_page = 5
    fieldsets = (
        (None, {
            "fields": (
                'email','username','password','device',
            ),
        }),
    )
    

    def get_queryset(self, request):
        return RestaurantManager.objects.filter(is_staff= True, is_superuser = False)
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()    

@admin.register(Customer)
class CustomCustomer(admin.ModelAdmin):
    model = Admin
    list_display = ["id",'email','username']
    list_editable = ['username']
    empty_value_display = 'empty'
    list_display_links = ['email']
    list_filter = ['email']
    search_fields = ('username','email')
    date_directly = ['date_joined']
    list_per_page = 5
    fieldsets = (
        (None, {
            "fields": (
                'email','username','password','device',
            ),
        }),
    )
    

    def get_queryset(self, request):
        return RestaurantManager.objects.filter(is_staff= False)
        
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()    

   


  



