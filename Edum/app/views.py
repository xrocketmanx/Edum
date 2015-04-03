"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import *

def courses(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/courses.html',
        context_instance = RequestContext(request,
        {
            'courses': Course.objects.all()
        })
    )

def course(request, course_id):
    assert isinstance(request, HttpRequest)
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        'app/course.html',
        context_instance = RequestContext(request,
        {
            'course': course
        })
    )

def module(request, course_id, module_id):
    assert isinstance(request, HttpRequest)
    module = get_object_or_404(Module, id=module_id)
    return render(
        request,
        'app/module.html',
        context_instance = RequestContext(request,
        {
            'module': module
        })
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'time':datetime.now(),
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html'
    )
