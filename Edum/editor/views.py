# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from app.models import *
from editor.forms import *
from django.core.context_processors import csrf

def merge_course(request, action, course_id):
    assert isinstance(request, HttpRequest)
    if action=='add':
        if request.POST:
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save()
    if action=='update':
        if request.POST:
            course = get_object_or_404(Course, id=course_id)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
    return redirect("/editor/courses/%s" % (course.id))

def merge_module(request, course_id, action, module_id):
    assert isinstance(request, HttpRequest)
    if action=='add':
        if request.POST:
            module = Module()
            module.name = request.POST['name']
            module.overview = request.POST['overview']
            module.course = get_object_or_404(Course, id=course_id)
            module.save()
    if action=='update':
        if request.POST:
            module = get_object_or_404(Module, id=module_id)
            form = ModuleForm(request.POST, instance=module)
            if form.is_valid():
                form.save()
    return redirect("/editor/courses/%s/modules" % (course_id))

def merge_lecture(request, module_id, action, lecture_id):
    assert isinstance(request, HttpRequest)
    if action=='add':
        if request.POST:
            lecture = Lecture()
            lecture.name = request.POST['name']
            lecture.video_url = request.POST['video_url']
            lecture.module = get_object_or_404(Module, id=module_id)
            lecture.save()
    if action=='update':
        if request.POST:
            lecture = get_object_or_404(Lecture, id=lecture_id)
            form = LectureForm(request.POST, instance=lecture)
            if form.is_valid():
                form.save()
    return redirect("/editor/courses/%s/modules/%s/lectures" % (lecture.module.course.id, module_id))

def edit_course(request, course_id):
    assert isinstance(request, HttpRequest)
    course = get_object_or_404(Course, id=course_id)
    course_form = CourseForm(instance=course)
    return render(
        request,
        'course_editor.html',
        context_instance = RequestContext(request,
        {
            'course_form': course_form,
            'course_id': course_id,
            'csrf_token': csrf(request),
        })
    )

def edit_modules(request, course_id):
    assert isinstance(request, HttpRequest)
    modules = Module.objects.filter(course_id=course_id)
    forms = [ ModuleForm(instance=module) for module in modules ]
    for module, form in zip(modules, forms):
        form.module_id = module.id
    return render(
        request,
        'module_editor.html',
        context_instance = RequestContext(request,
        {
            'forms': forms,
            'course_id': course_id,
            'module_form': ModuleForm,
            'csrf_token': csrf(request),
        })
    )

def edit_lectures(request, course_id, module_id):
    assert isinstance(request, HttpRequest)
    lectures = Lecture.objects.filter(module_id=module_id)
    forms = [ LectureForm(instance=lecture) for lecture in lectures ]
    for lecture, form in zip(lectures, forms):
        form.lecture_id = lecture.id
    return render(
        request,
        'lecture_editor.html',
        context_instance = RequestContext(request,
        {
            'forms': forms,
            'module_id': module_id,
            'lecture_form': LectureForm,
            'csrf_token': csrf(request),
        })
    )