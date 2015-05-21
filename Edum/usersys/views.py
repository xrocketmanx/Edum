from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from usersys.forms import RegistrationForm, ConfirmationToken, PetitionForm

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def login(request):
    message = ""
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect("home")
            else:
                message = "You need to confirm your email."
        else:
            message = "Wrong credentials, try again."
    return render(request,
        'login.html',
        context_instance = RequestContext(request,
        {
            'form': AuthenticationForm,
            'csrf_token': csrf(request),
            'message': message
         }))

def register(request):
    if request.user.is_authenticated():
        return redirect("courses") # or user profile
    message = ""
    if request.POST:
        form = RegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect("success")
        except ValidationError as error:
            message = error.args[0]
    return render(request,
        'register.html',
        context_instance = RequestContext(request,
        {
            'form': RegistrationForm,
            'message': message,
            'csrf_token': csrf(request),
         }))

def login_partial(request):
    return render_to_string('loginpartial.html',
        context_instance = RequestContext(request,
        {
            'user': request.user,
            'csrf_token': csrf(request),
        }))

@login_required()
def logout(request):
    if request.POST:
       django_logout(request)
    return redirect("home") 

def user_confirmation(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    confirmation_token = user.user_token
    if confirmation_token.token == token:
        confirmation_token.delete()
        user.is_active = True
        return redirect("login") 
    return redirect("home")

def success(request):
    user = request.user
    if user.is_authenticated():
        return redirect("courses")
    return render(request,
        'success.html',
        context_instance = RequestContext(request,
        {
         }))

@login_required(login_url="login")
def petition(request):
    message = None
    if request.POST:
        form = PetitionForm(request.POST)
        message = "Something went wrong"
        if form.is_valid():
            form.submit(request.user.username)
            message = "Successfuly sent petition"
    return render(request,
        'petition.html',
        context_instance = RequestContext(request,
        {
            'form': PetitionForm, 
            'message': message,
            'csrf_token': csrf(request),
        }
        )
    )


def accept_petition(request, username):
    user = get_object_or_404(User, username = username)
    teachers = Group.objects.get(name = 'teachers')
    teachers.user_set.add(user)
    return redirect('home')

