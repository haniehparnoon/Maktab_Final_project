from django.http import request
from django.shortcuts import render,  redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import *
from accounts.models import *
from .decorators import superuser_required, is_staff_required, customer_required
from django.db.models.aggregates import Count, Sum
from .forms import FoodForm, CategoryForm
import jdatetime

# Create your views here.
@superuser_required()
class AdminHome(CreateView):
    model = Food
    template_name = 'restaurant\home_admin.html'
    form_class = FoodForm
    success_url = reverse_lazy('Foods')

@superuser_required()
class FoodList(ListView):
    model = Food
    template_name = 'restaurant\Foods.html'

@superuser_required()
class EditFood(UpdateView):
    model = Food
    form_class = FoodForm
    template_name = 'restaurant\editfood.html'
    success_url = reverse_lazy('Foods')


@superuser_required()
class DeleteFood(DeleteView):
    model = Food
    template_name = 'restaurant\deletefood.html'
    success_url = reverse_lazy('Foods')

@superuser_required()
class AddCategory(CreateView):
    model = Category
    template_name = 'restaurant\category_add.html'
    form_class = CategoryForm
    success_url = reverse_lazy('Foods')

@is_staff_required()
class ManagerHome(TemplateView):
    template_name = 'restaurant\manager_home.html' 
       
@customer_required()
class CustomerHome(TemplateView):
    template_name = 'restaurant\customer_home.html'  

class BranchList(ListView):
    model = Branch
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        #best-selling foods
        foods = Food.objects.filter(food_menu__menu_order_item__order_id__status_id__status__contains='complete')
        best_selling_foods = foods.annotate(total= Sum('food_menu__menu_order_item__quantity')).order_by('-total')[:10]   
        #best-selling restaurants
        branches = Branch.objects.filter(menu__menu_order_item__order_id__status_id__status__contains='complete')
        best_selling_restaurants=branches.annotate(total = Sum('menu__menu_order_item__quantity')).order_by('-total')[:10]
        data = super().get_context_data(**kwargs)
        data['best_selling_foods'] = best_selling_foods
        data['best_selling_restaurants'] = best_selling_restaurants
        return data

class menuRestaurant(ListView):
    model = Menu
      
    template_name = 'restaurant\menurestaurant.html'
    def get_queryset(self, *args, **kwargs):
       # print(Menu.objects.filter(branch=self.kwargs['pk']))
        return Menu.objects.filter(branch=self.kwargs['pk'])


def menu_item(request,pk):
    food = Menu.objects.get(id = pk)
    if request.method == "POST":
        food = Menu.objects.get(id = pk)
        if request.user.is_authenticated :
            customer = request.user
        else:    
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device, username = device)
        if food.quantity >= int(request.POST['quantity']):
            status = OrderStatus.objects.get(status = "ordered")
            order, created = Order.objects.get_or_create(customer = customer, status_id =status)
            orderItem, created = OrderItem.objects.get_or_create(order_id=order, menu_id=food, quantity=1 )
            orderItem.quantity = request.POST['quantity']
            orderItem.save()
            return redirect('home')
        else:
            context = {'food':food, 'message':"Sorry :/"}
            return(request,'restaurant\menu_item.html',context)    
    context = {'food':food}
    return render(request,'restaurant\menu_item.html', context)


def cart(request):
    if request.user.is_authenticated :
        customer = request.user
        status = OrderStatus.objects.get(status = "ordered")
        order, created = Order.objects.get_or_create(customer=customer, status_id =status)
    else:  
        print("Hiiiii")  
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device, username = device)
        
        print(customer)
        status = OrderStatus.objects.get(status = "ordered")
        order = Order.objects.get(customer=customer, status_id =status)
        print(order) 
    context = {'order':order}
    return render(request,'restaurant/cart.html',context)

class OrderItemDelete(DeleteView):
    model = OrderItem
    template_name = 'restaurant\orderitem_delete.html'
    success_url = reverse_lazy('cart')

	





