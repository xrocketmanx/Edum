# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from app.models import *
from editor.forms import *
from django.core.context_processors import csrf
from usersys.views import login_partial

def merge_course(request, action, course_id):
    assert isinstance(request, HttpRequest)
    if request.POST:
        if action=='add':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save()
        if action=='update':
            course = get_object_or_404(Course, id=course_id)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
        if action=='delete':
            Course.objects.get(id=course_id).delete()
            return redirect("/courses")
    return redirect("/editor/courses/%s" % (course.id))

def merge_module(request, course_id, action, module_id):
    assert isinstance(request, HttpRequest)
    if request.POST:
        if action=='add':
            form = ModuleForm(request.POST)
            if form.is_valid():
                module = form.save(commit=False)
                module.course = get_object_or_404(Course, id=course_id)
                module.save()
        if action=='update':
            module = get_object_or_404(Module, id=module_id)
            form = ModuleForm(request.POST, instance=module)
            if form.is_valid():
                form.save()
        if action=='delete':
            Module.objects.get(id=module_id).delete()
    return redirect("/editor/courses/%s/modules" % (course_id))

def merge_lecture(request, module_id, action, lecture_id):
    assert isinstance(request, HttpRequest)
    if request.POST:
        if action=='add':
            form = LectureForm(request.POST)
            if form.is_valid():
                lecture = form.save(commit=False)
                lecture.module = get_object_or_404(Module, id=module_id)
                lecture.save()
        if action=='update':
            lecture = get_object_or_404(Lecture, id=lecture_id)
            form = LectureForm(request.POST, instance=lecture)
            if form.is_valid():
                form.save()
        if action=='delete':
            Lecture.objects.get(id=lecture_id).delete()
    return redirect("/editor/courses/%s/modules/%s/lectures" % (lecture.module.course.id, module_id))

def merge_test(request, module_id, action, test_id):
    assert isinstance(request, HttpRequest)
    if request.POST:
        if action=='add':
            form = TestForm(request.POST)
            if form.is_valid():
                test = form.save(commit=False)
                test.module = get_object_or_404(Module, id=module_id)
                test.save()
        if action=='update':
            #lecture = get_object_or_404(Lecture, id=lecture_id)
            #form = LectureForm(request.POST, instance=lecture)
            #if form.is_valid():
            #    form.save()
            pass
        if action=='delete':
            Test.objects.get(id=test_id).delete()
            return redirect("/editor/courses/%s/modules/%s/tests" % (test.module.course.id, module_id))
    return redirect("/editor/courses/%s/modules/%s/tests/%s" % (test.module.course.id, module_id, test.id))

# 

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
            'loginpartial': login_partial(request),
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
            'loginpartial': login_partial(request),
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
            'loginpartial': login_partial(request),
        })
    )

def edit_tests(request, course_id, module_id):
    assert isinstance(request, HttpRequest)
    tests = Test.objects.filter(module_id=module_id)
    forms = [ TestForm(instance=test) for test in tests ]
    for test, form in zip(tests, forms):
        form.test_id = test.id
    return render(
        request,
        'tests_editor.html',
        context_instance = RequestContext(request,
        {
            'forms': forms,
            'course_id': course_id,
            'module_id': module_id,
            'test_form': TestForm,
            'csrf_token': csrf(request),
            'loginpartial': login_partial(request),
        })
    )

def edit_test(request, course_id, module_id, test_id):
    assert isinstance(request, HttpRequest)
    test = get_object_or_404(Test, id=test_id)
    test_form = TestForm(instance=test)
    test_form.test_id = test_id
    return render(
        request,
        'test_editor.html',
        context_instance = RequestContext(request,
        {
            'test_form': test_form,
            'course_id': course_id,
            'module_id': module_id,
            'question_form': QuestionForm,
            'answer_form': AnswerForm,
            'csrf_token': csrf(request),
            'loginpartial': login_partial(request),
        })
    )