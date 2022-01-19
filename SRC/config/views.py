
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def wherenext(request):

    """Simple redirector to figure out where the user goes next after login."""
    if request.user.is_superuser :
        return redirect(reverse('home_admin'))
    elif request.user.is_staff and not(request.user.is_superuser):
        return redirect(reverse('home_manager'))
    elif not(request.user.is_staff) and not(request.user.is_superuser):
        return redirect(reverse('home_customer'))