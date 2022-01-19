from django.urls import path
from .views import *
from allauth.account.views import LoginView, SignupView 



urlpatterns = [
    path('signup/Admin/',view = admin_signup, name='signup_admin'),
     
]