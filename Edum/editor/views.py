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
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from editor.editors import *

#Course editing

@group_required('teachers')
def create_course(request):
    if request.POST:
        course = course_editor.create(request.POST, author=request.user)
        if course:
            return redirect('edit_course', course_id=course.id)
    return redirect('courses')

@group_required('teachers')
def update_course(request, pk):
    if request.POST:
        course_editor.update(request.POST, pk)
    return redirect('edit_course', course_id=pk)

@group_required('teachers')
def delete_course(request, pk):
    if request.POST:
        course_editor.delete(pk)
    return redirect('courses')

#Module editing

@group_required('teachers')
def create_module(request, course_id):
    course = course_editor.get_model(course_id)
    if request.POST:
        module_editor.create(request.POST, course=course)
    return redirect('edit_modules', course_id=course_id)

@group_required('teachers')
def update_module(request, course_id, pk):
    if request.POST:
        module_editor.update(request.POST, pk)
    return redirect('edit_modules', course_id=course_id)

@group_required('teachers')
def delete_module(request, course_id, pk):
    if request.POST:
        module_editor.delete(pk)
    return redirect('edit_modules', course_id=course_id)

#Lecture editing TODO:add duration to course

@group_required('teachers')
def create_lecture(request, module_id):
    module = module_editor.get_model(module_id)
    if request.POST:
        lecture_editor.create(request.POST, module=module)
    return redirect('edit_lectures', module_id=module.id, course_id=module.course.id)

@group_required('teachers')
def update_lecture(request, module_id, pk):
    module = module_editor.get_model(module_id)
    if request.POST:
        lecture_editor.update(request.POST, pk)
    return redirect('edit_lectures', module_id=module.id, course_id=module.course.id)

@group_required('teachers')
def delete_lecture(request, module_id, pk):
    module = module_editor.get_model(module_id)
    if request.POST:
        lecture_editor.delete(pk)
    return redirect('edit_lectures', module_id=module.id, course_id=module.course.id)

#Test editing

@group_required('teachers')
def create_test(request, module_id):
    module = module_editor.get_model(module_id)
    if request.POST:
        test_editor.create(request.POST, module=module)
    return redirect('edit_tests', module_id=module.id, course_id=module.course.id)

@group_required('teachers')
def update_test(request, module_id, pk):
    module = module_editor.get_model(module_id)
    if request.POST:
        test_editor.update(request.POST, pk)
    return redirect('edit_tests', module_id=module.id, course_id=module.course.id)

@group_required('teachers')
def delete_test(request, module_id, pk):
    module = module_editor.get_model(module_id)
    if request.POST:
        test_editor.delete(pk)
    return redirect('edit_tests', module_id=module.id, course_id=module.course.id)

#Question editing

def create_question(request, test_id):
    test = test_editor.get_model(test_id)
    if request.POST:
        question_editor.create(request.POST, test=test)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

@group_required('teachers')
def update_question(request, test_id, pk):
    test = test_editor.get_model(test_id)
    if request.POST:
        question_editor.update(request.POST, pk)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

@group_required('teachers')
def delete_question(request, test_id, pk):
    test = test_editor.get_model(test_id)
    if request.POST:
        question_editor.delete(pk)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

#Answer editing

def create_answer(request, question_id):
    question = question_editor.get_model(question_id)
    test = question.test
    if request.POST:
        answer_editor.create(request.POST, question=question)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

@group_required('teachers')
def update_answer(request, question_id, pk):
    question = question_editor.get_model(question_id)
    test = question.test
    if request.POST:
        answer_editor.update(request.POST, pk)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

@group_required('teachers')
def delete_answer(request, question_id, pk):
    question = question_editor.get_model(question_id)
    test = question.test
    if request.POST:
        answer_editor.delete(pk)
    return redirect('edit_test', test_id=test.id, module_id=test.module.id, course_id=test.module.course.id)

#Editor views

class EditCourse(TemplateView):
    template_name = 'course_editor.html'
    form_class = CourseForm

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=kwargs['course_id'])
        if is_not_author(request, course.id):
            return redirect('forbidden')
        form = self.get_form(course)
        return self.render_to_response(
            self.get_context_data(
                course_form=form, 
                course=course,
                loginpartial=login_partial(request)
            )
        )

    def get_form(self, course):
        return self.form_class(instance=course)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EditModules(TemplateView):
    form_class = ModuleForm
    template_name = 'module_editor.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id'] 
        if is_not_author(request, course_id):
            return redirect('forbidden')
        forms = self.get_forms(course_id)
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response(
            self.get_context_data(
                forms=forms,
                module_form=self.form_class, 
                course=course,
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
        course_id = kwargs['course_id'] 
        if is_not_author(request, course_id):
            return redirect('forbidden')
        forms = self.get_forms(kwargs['module_id'])
        module = get_object_or_404(Module, id=kwargs['module_id'])
        return self.render_to_response(
            self.get_context_data(
                forms=forms,
                lecture_form=self.form_class, 
                module=module,
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

class EditTests(TemplateView):
    form_class = TestForm
    template_name = 'tests_editor.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id'] 
        if is_not_author(request, course_id):
            return redirect('forbidden')
        forms = self.get_forms(kwargs['module_id'])
        module = get_object_or_404(Module, id=kwargs['module_id'])
        return self.render_to_response(
            self.get_context_data(
                forms=forms,
                module=module,
                test_form=self.form_class, 
                loginpartial=login_partial(request)
            )
        )

    def get_forms(self, module_id):
        tests = Test.objects.filter(module_id=module_id)
        forms = [ TestForm(instance=test) for test in tests ]
        for test, form in zip(tests, forms):
            form.test_id = test.id
        return forms

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EditTest(TemplateView):
    form_class = TestForm
    template_name = 'test_editor.html'

    def get(self, request, *args, **kwargs):
        test = get_object_or_404(Test, id=kwargs['test_id'])
        if is_not_author(request, test.module.course.id):
            return redirect('forbidden')
        test_form = self.get_form(test)
        question_forms = self.get_question_forms(test.id)

        return self.render_to_response(
            self.get_context_data(
                test_form=test_form,
                course=test.module.course,
                module=test.module,
                test=test,
                question_form=QuestionForm,
                answer_form=AnswerForm,
                question_forms=question_forms,
                loginpartial=login_partial(request),
            )
        )

    def get_form(self, test):
       return self.form_class(instance=test)
   
    def get_question_forms(self, test_id):
       questions = Question.objects.filter(test_id=test_id)
       question_forms = [ QuestionForm(instance=question) for question in questions ]
       for question, form in zip(questions, question_forms):
            form.answers = self.get_answer_forms(question.id)
            form.question_id = question.id
       return question_forms

    def get_answer_forms(self, question_id):
       answers = Answer.objects.filter(question_id=question_id)
       answer_forms = [ AnswerForm(instance=answer) for answer in answers ]
       for answer, form in zip(answers, answer_forms):
            form.answer_id = answer.id
       return answer_forms

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def is_not_author(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if course.author.id == user.id:
        return False
    return True