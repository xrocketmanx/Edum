# -*- encoding: utf-8 -*-
import json
from datetime import datetime, timedelta
from random import shuffle
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from Edum.shortcuts import render
from app.utils import *
from app.models import *
from editor.forms import *

@csrf_protect
def courses(request):
    editing_permission = is_teacher(request.user)

    page = request.GET.get('page')
    courses = Paginator(Course, 5).page(page)
    return render(
        request,
        'app/courses.html',
        {
            'is_authenticated': request.user.is_authenticated(),
            'editing_permission': editing_permission,
            'courses': courses,
            'course_form': CourseForm,
        }
    )

def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    update_course_duration(course)
    progress = 0
    if request.user.is_authenticated():
        user_profile = request.user.user_profile
        update_course_progress(course, user_profile)
        progress = get_course_progress(user_profile, course)
    return render(
        request,
        'app/course.html',
        {
            'progress': progress,
            'is_authenticated': request.user.is_authenticated(),
            'course': course,
        }
    )

@login_required()
def subscribe(request, course_id):
    user_profile = request.user.user_profile
    course = get_object_or_404(Course, id=course_id)
    progress = CourseProgress(user=user_profile, course=course)
    progress.save()

    return redirect("course", course_id)

@login_required()
@is_subscribed
def unsubscribe(request, course_id):
    user_profile = request.user.user_profile
    course = get_object_or_404(Course, id=course_id)
    progress = get_object_or_404(CourseProgress, user=user_profile, course=course)
    progress.delete()

    return redirect("courses")

@login_required()
@is_subscribed
def module(request, course_id, module_id):
    module = get_object_or_404(Module, id=module_id)
    return render(
        request,
        'app/module.html',
        {
            'module': module,
        }
    )

@login_required()
@is_subscribed
def lecture(request, course_id, module_id, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    return render(
        request,
        'app/lecture.html',
        {
            'lecture': lecture,
        }
    )

@login_required()
@is_subscribed
def test(request, course_id, module_id, test_id):
    test = get_object_or_404(Test, id=test_id)
    if test.module.id != int(module_id):
        raise Http404("Lecture not found")
    return render(
        request,
        'app/test.html',
        {
            'test': test,
        }
    )

@login_required()
@is_subscribed
def start_test(request, course_id, test_id):
    test = get_object_or_404(Test, id=test_id)
    duration = test.duration * 60 * 1000

    return render(
        request,
        'app/testing.html',
        {
            'test': test,
            'duration': duration,
        }
    )

def home(request):
    return render(
        request,
        'app/home.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def contact(request):
    return render(
        request,
        'app/contact.html',
        {
            'time': datetime.now(),
        }
    )

def about(request):
    return render(
        request,
        'app/about.html',
    )

def forbidden(request):
    return render(
        request,
        'app/403-page.html'
    )

@login_required()
@is_subscribed
def get_questions(request, course_id, test_id):
    test = get_object_or_404(Test, id=test_id)
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
@is_subscribed
def get_test_result(request, course_id, test_id):
    test = get_object_or_404(Test, id=test_id)

    user_results = json.loads(request.POST['results'])
    user_grade = calculate_grade(user_results, test.questions.all())
    save_test_result(user_grade, request.user.user_profile, test)

    return HttpResponse(
        user_grade,
        content_type="application/text"
    )

def save_test_result(user_grade, user_profile, test):
    test_results = TestResult.objects.filter(test=test, user=user_profile)
    passed = False if user_grade < 0.7 else True
    if len(test_results) > 0:
        test_result = test_results[0]
        if passed or test_result.passed:
            test_result.passed = True
        else:
            test_result.passed = False
    else:
        test_result = TestResult()
        test_result.test = test
        test_result.user = user_profile
        test_result.passed = passed
    test_result.save()

@login_required()
@is_subscribed
def like_course(request, course_id):
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
    return HttpResponse(
        course.rating,
        content_type="text/plain"
    )