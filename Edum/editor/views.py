# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import * # remove later
from django.template import RequestContext
from app.models import *
from editor.forms import *
from django.core.context_processors import csrf
from usersys.views import login_partial
from django.contrib.auth.decorators import login_required
from usersys.views import group_required
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

@group_required('teachers')
def merge_course(request, action, course_id):
    if request.POST:
        if action == 'add':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save()
        if action == 'update':
            course = get_object_or_404(Course, id=course_id)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
        if action == 'delete':
            Course.objects.get(id=course_id).delete()
            return redirect("courses")
    return redirect("edit_course", course_id=course.id)

@group_required('teachers')
def merge_module(request, course_id, action, module_id):
    if request.POST:
        if action == 'add':
            form = ModuleForm(request.POST)
            if form.is_valid():
                module = form.save(commit=False)
                module.course = get_object_or_404(Course, id=course_id)
                module.save()
        if action == 'update':
            module = get_object_or_404(Module, id=module_id)
            form = ModuleForm(request.POST, instance=module)
            if form.is_valid():
                form.save()
        if action == 'delete':
            Module.objects.get(id=module_id).delete()
    return redirect("edit_modules", course_id=course_id)

@group_required('teachers')
def merge_lecture(request, module_id, action, lecture_id):
    if request.POST:
        if action == 'add':
            form = LectureForm(request.POST)
            if form.is_valid():
                lecture = form.save(commit=False)
                lecture.module = get_object_or_404(Module, id=module_id)
                lecture.save()
        if action == 'update':
            lecture = get_object_or_404(Lecture, id=lecture_id)
            form = LectureForm(request.POST, instance=lecture)
            if form.is_valid():
                form.save()
        if action == 'delete':
            Lecture.objects.get(id=lecture_id).delete()
    return redirect("edit_lectures", course_id=lecture.module.course.id, module_id=module_id)

@group_required('teachers')
def merge_test(request, module_id, action, test_id):
    if request.POST:
        if action == 'add':
            form = TestForm(request.POST)
            if form.is_valid():
                test = form.save(commit=False)
                test.module = get_object_or_404(Module, id=module_id)
                test.save()
        if action == 'update':
            #lecture = get_object_or_404(Lecture, id=lecture_id)
            #form = LectureForm(request.POST, instance=lecture)
            #if form.is_valid():
            #    form.save()
            pass
        if action == 'delete':
            Test.objects.get(id=test_id).delete()
            return redirect("edit_tests", course_id=test.module.course.id, module_id=module_id)
    return redirect("edit_test", course_id=test.module.course.id, module_id=module_id, test_id=test.id)

class EditCourse(TemplateView):
    template_name = 'course_editor.html'
    form_class = CourseForm

    def get(self, request, *args, **kwargs):
        form = self.get_form(kwargs['course_id'])
        return self.render_to_response(
            self.get_context_data(
                course_form=form, 
                course_id=kwargs['course_id'],
                loginpartial=login_partial(request)
            )
        )

    def get_form(self, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.form_class(instance=course)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EditModules(TemplateView):
    form_class = ModuleForm
    template_name = 'module_editor.html'

    def get(self, request, *args, **kwargs):
        forms = self.get_forms(kwargs['course_id'])
        return self.render_to_response(
            self.get_context_data(
                forms=forms,
                module_form=self.form_class, 
                course_id=kwargs['course_id'],
                loginpartial=login_partial(request)
            )
        )

    def get_forms(self, course_id):
        modules = Module.objects.filter(course_id=course_id)
        forms = [ ModuleForm(instance=module) for module in modules ]
        for module, form in zip(modules, forms):
            form.module_id = module.id
        return forms

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EditLectures(TemplateView):
    form_class = LectureForm
    template_name = 'lecture_editor.html'

    def get(self, request, *args, **kwargs):
        forms = self.get_forms(kwargs['module_id'])
        return self.render_to_response(
            self.get_context_data(
                forms=forms,
                lecture_form=self.form_class, 
                module_id=kwargs['module_id'],
                loginpartial=login_partial(request)
            )
        )
 
    def get_forms(self, module_id):
        lectures = Lecture.objects.filter(module_id=module_id)
        forms = [ LectureForm(instance=lecture) for lecture in lectures ]
        for lecture, form in zip(lectures, forms):
            form.lecture_id = lecture.id
        return forms

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@group_required('teachers')
def edit_tests(request, course_id, module_id):
    tests = Test.objects.filter(module_id=module_id)
    forms = [ TestForm(instance=test) for test in tests ]
    for test, form in zip(tests, forms):
        form.test_id = test.id
    return render(request,
        'tests_editor.html',
        context_instance = RequestContext(request,
        {
            'forms': forms,
            'course_id': course_id,
            'module_id': module_id,
            'test_form': TestForm,
            'csrf_token': csrf(request),
            'loginpartial': login_partial(request),
        }))

@group_required('teachers')
def edit_test(request, course_id, module_id, test_id):
    test = get_object_or_404(Test, id=test_id)
    test_form = TestForm(instance=test)
    test_form.test_id = test_id
    return render(request,
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
        }))
