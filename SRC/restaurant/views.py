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






