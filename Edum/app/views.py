# -*- encoding: utf-8 -*-
import json
from random import shuffle
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from datetime import datetime, timedelta
from app.models import *
from editor.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core import serializers
from usersys.views import login_partial

def courses(request):
    user = request.user
    editing_permission_groups = user.groups.filter(name='teachers')
    editing_permission = False
    if len(editing_permission_groups) > 0:
        editing_permission = True
    return render(
        request,
        'app/courses.html',
        context_instance = RequestContext(request,
        {
            'is_authenticated': user.is_authenticated(),
            'editing_permission': editing_permission,
            'courses': Course.objects.all(),
            'course_form': CourseForm,
            'csrf_token': csrf(request),
            'loginpartial': login_partial(request),
        })
    )

def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        'app/course.html',
        context_instance = RequestContext(request,
        {
            'is_authenticated': request.user.is_authenticated(),
            'course': course,
            'loginpartial': login_partial(request),
        })
    )

@login_required()
def like_course(request, course_id, view_name):
    if request.POST:
        user = request.user
        course = get_object_or_404(Course, id=course_id)
        user_likes = CoursesLikes.objects.filter(user=user, course=course)
        if len(user_likes) > 0:
            course.rating -= 1
            user_likes[0].delete()
        else:
            course.rating += 1
            course_like = CoursesLikes(user=user, course=course)
            course_like.save()
        course.save()
        if view_name == "course":
            return redirect(view_name, course_id=course_id)
    return redirect("courses")

@login_required()
def subscribe(request, course_id):
    user_profile = request.user.user_profile
    course = get_object_or_404(Course, id=course_id)
    progress = CourseProgress(user=user_profile, course=course)
    progress.save()

    return redirect("course", course_id)

@login_required()
def unsubscribe(request, course_id):
    user_profile = request.user.user_profile
    course = get_object_or_404(Course, id=course_id)
    progress = get_object_or_404(CourseProgress, user=user_profile, course=course)
    progress.delete()

    return redirect("courses")

@login_required()
def module(request, course_id, module_id):
    if not subscribed(request.user, course_id):
        return redirect("forbidden")
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
    if not subscribed(request.user, course_id):
        return redirect("forbidden")
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
    if not subscribed(request.user, course_id):
        return redirect("forbidden")
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

@login_required()
def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if not subscribed(request.user, test.module.course.id):
        return redirect("forbidden")
    duration = test.duration * 60 * 1000

    return render(
        request,
        'app/testing.html',
        context_instance = RequestContext(request,
        {
            'test': test,
            'duration': duration,
            'loginpartial': login_partial(request),
        })
    )

@login_required()
def get_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if not subscribed(request.user, test.module.course.id):
        return redirect("forbidden")
    data = {}

    test_questions = [ question for question in test.questions.all() ]

    shuffle(test_questions)
    test_questions = test_questions[:test.question_count]

    for question in test_questions:
        data[question.text] = [ answer.text for answer in question.answers.all() ]

    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )

@csrf_exempt
@login_required()
def get_test_result(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if not subscribed(request.user, test.module.course.id):
        return redirect("forbidden")

    user_results = json.loads(request.POST['results'])
    user_grade = calculate_grade(user_results, test.questions.all())

    test_result = TestResult()
    test_result.test = test
    test_result.user = request.user.user_profile
    test_result.passed = False if user_grade < 0.7 else True
    test_result.save()

    return HttpResponse(
        user_grade,
        content_type="application/text"
    )

def calculate_grade(user_results, test_questions):
    user_grade = 0
    for question in user_results:
        test_question = test_questions.get(text=question['text'])
        if(is_correct(question['answers'], test_question)):
            user_grade += 1
    return user_grade / len(test_questions)

def is_correct(answers, question):
    for answer in question.answers.all():
        if answer.correct:
            if answer.text not in answers:
                return False
        else:
            if answer.text in answers:
                return False
    return True

def home(request):
    """Renders the home page."""
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
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'loginpartial': login_partial(request),
        })
    )

def forbidden(request):
    return render(
        request,
        'app/403-page.html',
        context_instance = RequestContext(request,
        {
            'loginpartial': login_partial(request),
        })
    )

def subscribed(user, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course in user.user_profile.signed_courses.all():
        return True
    return False