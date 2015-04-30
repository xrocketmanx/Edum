# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from usersys.forms import RegistrationForm, ConfirmationToken

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect("/")
                # Redirect to a success page.
            else:
                return redirect("/users/login")
                # Return a 'disabled account' error message
        else:
            return redirect("/users/login")
            # Return an 'invalid login' error message.
    return render(request,
        'login.html',
        context_instance = RequestContext(request,
        {
            'form': AuthenticationForm,
            'csrf_token': csrf(request),
         })
    )

def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
    return render(request,
        'register.html',
        context_instance = RequestContext(request,
        {
            'form': RegistrationForm,
            'csrf_token': csrf(request),
         })
    )

def login_partial(request):
    return render_to_string(
        'loginpartial.html',
        context_instance = RequestContext(request,
        {
            'user': request.user,
            'csrf_token': csrf(request),
        })
    )

def logout(request):
    if request.POST:
       django_logout(request)
    return redirect("/") 

def user_confirmation(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    confirmation_token = user.user_token
    if confirmation_token.token == token:
        confirmation_token.delete()
        user.is_active = True
        return redirect("/courses")
    return redirect("/")