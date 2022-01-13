from django.forms import fields
from django.http import request
from django.shortcuts import render,  redirect
from django.urls.base import reverse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import *
from accounts.models import *
from .decorators import superuser_required, is_staff_required, customer_required
from django.db.models.aggregates import Count, Sum
from .forms import FoodForm, CategoryForm
import jdatetime
from django.db.models import Q
from django.http import JsonResponse
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
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


       
  

class BranchList(ListView,APIView):
    model = Branch
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        #best-selling foods
        foods = Food.objects.filter(Q(food_menu__menu_order_item__order_id__status_id__status__contains='complete')|
        Q(food_menu__menu_order_item__order_id__status_id__status__contains='sent')|
        Q(food_menu__menu_order_item__order_id__status_id__status__contains='delivered') )
        best_selling_foods = foods.annotate(total= Sum('food_menu__menu_order_item__quantity')).order_by('-total')[:10]   
        #best-selling restaurants
        branches = Branch.objects.filter(Q(menu__menu_order_item__order_id__status_id__status__contains='complete')|Q(menu__menu_order_item__order_id__status_id__status__contains='sent')|Q(menu__menu_order_item__order_id__status_id__status__contains='delivered'))
        best_selling_restaurants=branches.annotate(total = Sum('menu__menu_order_item__quantity')).order_by('-total')[:10]
        data = super().get_context_data(**kwargs)
        data['best_selling_foods'] = best_selling_foods
        data['best_selling_restaurants'] = best_selling_restaurants
        return data

    def post(self, req):
        if req.method == 'POST'  and req.is_ajax():
            print("omad to shart")
            text = req.POST.get('search_input')
            print(text)
            if text :
                branch = Branch.objects.filter(name__contains=text)
                food = Food.objects.filter(name__contains=text)
                print("ffod",food)
                branches ={}
                foods ={}
                if branch:
                    serializer_branch = BranchSerializer(branch,many=True,context={'request': request})
                    branches = serializer_branch.data    
                    print("BBBBBBBBBBBBB:",branches)
                
                if food:
                    serializer_food = FoodSerializer(food,many=True,context={'request': request})
                    foods = serializer_food.data
                    print("FFFFFFFFFFFFF",foods)
                
                return Response({"branches":branches , "foods":foods})
                

            else:
                Response({"branches":[] , "foods":[],"msg":"does not match"})
              

        return render(req,'home.html')   





class menuRestaurant(ListView):
    model = Menu
      
    template_name = 'restaurant\menurestaurant.html'
    def get_queryset(self, *args, **kwargs):
        return Menu.objects.filter(branch=self.kwargs['pk'])


def menu_item(request,pk):
    food = Menu.objects.get(id = pk)
    selected_branch = food.branch
    selected_food = food.food
    existed_branch=''
    order_item_existed=''
    if request.method == "POST":
        food = Menu.objects.get(id = pk)
        selected_branch = food.branch
        if request.user.is_authenticated :
            customer = request.user
        else:    
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device, username = device)

        status = OrderStatus.objects.get(status = "ordered") 
        orders= Order.objects.filter(Q(customer = customer)& Q(status_id = status) ).last()
        print("order",orders)
        if orders:
            order_item_existed = OrderItem.objects.filter(order_id = orders).last()

        if order_item_existed :
            existed_food = Food.objects.filter(food_menu__menu_order_item=order_item_existed)
            existed_branch = Branch.objects.get(menu__menu_order_item =order_item_existed)

            if selected_food  in   existed_food:
                context = {'food':food, 'message':"this item already exist:/"}
                return render(request,'restaurant\menu_item.html',context)

        if existed_branch and not selected_branch.name == existed_branch.name:
            print("selected_branch ",selected_branch.name )
            print(type(selected_branch.name))
            print("existed_branch",existed_branch)
            #if not selected_branch.name == existed_branch.name:
            context = {'food':food, 'message':"you can only use from one branch or delete your cart "}
            return render(request,'restaurant\menu_item.html',context)

        else:    
            if food.quantity >= int(request.POST['quantity']):
                status = OrderStatus.objects.get(status = "ordered")
                order, created = Order.objects.get_or_create(customer = customer, status_id =status)
                orderItem, created = OrderItem.objects.get_or_create(order_id=order, menu_id=food, quantity=1 )
                orderItem.quantity = request.POST['quantity']
                orderItem.save()
                return redirect('cart')
            else:
                context = {'food':food, 'message':"Sorry  not enough food:/"}
                return render(request,'restaurant\menu_item.html',context)    
    context = {'food':food}
    return render(request,'restaurant\menu_item.html', context)

#____________________________________________________________Cart_________________________________________________________

def cart(request):
    if request.method == "POST":
        customer_address = request.POST.get("customer_address")
        pk,city,street,number =customer_address.split("_")
        print(pk)
        choosen_address = Address.objects.get(pk = pk)
        print(choosen_address)
        customer = request.user
        status = OrderStatus.objects.get(status = "ordered")
        new_status = OrderStatus.objects.get(status = "complete")
        order= Order.objects.filter(customer=customer, status_id =status).update(status_id=new_status)
        msg = "successfull"
        return render(request,'restaurant/cart.html',{"msg":msg})

        





    if request.user.is_authenticated :
        addresses = Address.objects.filter(customer_id = request.user)
        customer = request.user
        status = OrderStatus.objects.get(status = "ordered")
        device = request.COOKIES['device']
        customer_device = Customer.objects.filter(device=device, username = device).last()
        order, created = Order.objects.get_or_create(customer=customer, status_id =status)
        if customer_device:
            print("custooomerr",customer_device)
            order_device = Order.objects.filter(customer=customer_device, status_id =status).last()
            if order_device :
                order_items_device = OrderItem.objects.filter(order_id = order_device.id)
                if order_items_device:
                    Order.objects.filter(id = order.id).delete()
                    Order.objects.filter(id = order_device.id).update(customer = customer)
                    Customer.objects.filter(id = customer_device.id).delete()
                    order = Order.objects.filter(customer = customer , status_id = status).last()
                    
       
    else:  
        print("Hiiiii")  
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device, username = device)
        
        print(customer)
        status = OrderStatus.objects.get(status = "ordered")
        order,created = Order.objects.get_or_create(customer=customer, status_id =status)
    
  
    context = {'order':order,"addresses":addresses }
    print(order)
    return render(request,'restaurant/cart.html',context)


