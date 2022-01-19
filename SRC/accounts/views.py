from django.shortcuts import render
from .forms import *
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from allauth.account.views import SignupView

# class CustomerRegistrationView(SignupView):
#     template_name = 'allauth/accounts/signup.html'
#     form_class = CustomerSignupForm
#     redirect_field_name = 'next'
#     view_name = 'signup'
#     success_url = None

#     def get_context_data(self, **kwargs):
#         ret = super(CustomerRegistrationView, self).get_context_data(**kwargs)
#         ret.update(self.kwargs)
#         return ret

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     template_name = 'accounts/signup.html'

class AdminSignupView(SignupView):
    # The referenced HTML content can be copied from the signup.html
    # in the django-allauth template folder
    template_name =" accounts/signup_admin.html"
    # the previously created form class
    form_class = AdminSignupForm
    #redirect_field_name = 'next'

    # the view is created just a few lines below
    # N.B: use the same name or it will blow up
    view_name = 'admin_signup'

    # I don't use them, but you could override them
    # (N.B: the following values are the default)
    success_url = None
    # redirect_field_name = 'next'
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        return ret

# Create the view (we will reference to it in the url patterns)
admin_signup = AdminSignupView.as_view()


