# Create your views here.
from usersys.forms import BootstrapAuthenticationForm
from django.core.context_processors import csrf
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login

def login_page(request):
    return render(request,
        'login.html',
        context_instance = RequestContext(request,
        {
            'form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            },
            'csrf_token': csrf(request),
         })
    )

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return redirect("/")
            # Redirect to a success page.
        else:
            return redirect("/users/login_page")
            # Return a 'disabled account' error message
    else:
        return redirect("/users/login_page")
        # Return an 'invalid login' error message.
