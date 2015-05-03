# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from datetime import datetime
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from usersys.views import login_partial

def courses(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/courses.html',
        context_instance = RequestContext(request,
        {
            'courses': Course.objects.all(),
            'course_form': CourseForm,
            'csrf_token': csrf(request),
            'loginpartial': login_partial(request),
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
            'course': course,
            'loginpartial': login_partial(request),
        })
    )

@login_required()
def module(request, course_id, module_id):
    assert isinstance(request, HttpRequest)
    module = get_object_or_404(Module, id=module_id)
    if module.course.id != int(course_id):
        raise Http404("Module not found")
    return render(
        request,
        'app/module.html',
        context_instance = RequestContext(request,
        {
            'module': module,
            'loginpartial': login_partial(request),
        })
    )

@login_required()
def lecture(request, course_id, module_id, lecture_id):
    assert isinstance(request, HttpRequest)
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if lecture.module.course.id != int(course_id):
        raise Http404("Module not found")
    if lecture.module.id != int(module_id):
        raise Http404("Lecture not found")
    return render(
        request,
        'app/lecture.html',
        context_instance = RequestContext(request,
        {
            'lecture': lecture,
            'loginpartial': login_partial(request),
        })
    )

@login_required()
def test(request, course_id, module_id, test_id):
    assert isinstance(request, HttpRequest)
    test = get_object_or_404(Test, id=test_id)
    if test.module.course.id != int(course_id):
        raise Http404("Module not found")
    if test.module.id != int(module_id):
        raise Http404("Lecture not found")
    return render(
        request,
        'app/test.html',
        context_instance = RequestContext(request,
        {
            'test': test,
            'loginpartial': login_partial(request),
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
            'loginpartial': login_partial(request),
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
            'loginpartial': login_partial(request),
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'loginpartial': login_partial(request),
        })
    )



