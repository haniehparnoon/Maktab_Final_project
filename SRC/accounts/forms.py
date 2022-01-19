
from .models import Admin
from allauth.account.forms import SignupForm
from allauth.account import forms


class AdminSignupForm(SignupForm):
   
    def save(self, request):
       
        user = super(AdminSignupForm, self).save(request)
        user.is_superuser = True
        
    
        user.save()

    
        return user

  