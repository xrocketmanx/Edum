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

#Course editing

class CourseCreator(CreateView):
    model = Course
    success_url = 'edit_course'
    failure_url = 'courses'

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(False)
            course.author = request.user
            course.save()
            return redirect(self.success_url, course_id=course.id)
        return redirect(self.failure_url)
    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CourseUpdater(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = '/editor/courses/%s'

    def get_success_url(self):
        return self.success_url % self.object.id

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CourseDeleter(DeleteView):
    model = Course
    form_class = CourseForm
    success_url = '/courses'

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Module editing

class ModuleCreator(CreateView):
    model = Module
    success_url = 'edit_modules'

    def post(self, request, *args, **kwargs):
        form = ModuleForm(request.POST)
        course = get_object_or_404(Course, pk=kwargs['course_id'])
        if form.is_valid():
            module = form.save(False)
            module.course = course
            module.save()
        return redirect(self.success_url, course_id=course.id)

    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ModuleUpdater(UpdateView):
    model = Module
    form_class = ModuleForm
    success_url = '/editor/courses/%s/modules'

    def get_success_url(self):
        return self.success_url % (self.object.course.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ModuleDeleter(DeleteView):
    model = Module
    form_class = ModuleForm
    success_url = '/editor/courses/%s/modules'

    def get_success_url(self):
        return self.success_url % (self.object.course.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Lecture editing TODO: add duration to course

class LectureCreator(CreateView):
    model = Lecture
    success_url = 'edit_lectures'

    def post(self, request, *args, **kwargs):
        form = LectureForm(request.POST)
        module = get_object_or_404(Module, pk=kwargs['module_id'])
        course = module.course
        if form.is_valid():
            lecture = form.save(False)
            lecture.module = module
            lecture.save()
        return redirect(self.success_url, course_id=course.id, module_id=module.id)
    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class LectureUpdater(UpdateView):
    model = Lecture
    form_class = LectureForm
    success_url = '/editor/courses/%s/modules/%s/lectures'

    def get_success_url(self):
        return self.success_url % (self.object.module.course.id, self.object.module.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class LectureDeleter(DeleteView):
    model = Lecture
    form_class = LectureForm
    success_url = '/editor/courses/%s/modules/%s/lectures'

    def get_success_url(self):
        return self.success_url % (self.object.module.course.id, self.object.module.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Test editing

class TestCreator(CreateView):
    model = Test
    success_url = 'edit_tests'

    def post(self, request, *args, **kwargs):
        form = TestForm(request.POST)
        module = get_object_or_404(Module, pk=kwargs['module_id'])
        course = module.course
        if form.is_valid():
            test = form.save(False)
            test.module = module
            course.duration += test.duration / 60
            course.save()
            test.save()
        return redirect(self.success_url, course_id=course.id, module_id=module.id)
    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TestUpdater(UpdateView):
    model = Test
    form_class = TestForm
    success_url = '/editor/courses/%s/modules/%s/tests'

    def get_success_url(self):
        return self.success_url % (self.object.module.course.id, self.object.module.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TestDeleter(DeleteView):
    model = Test
    form_class = TestForm
    success_url = '/editor/courses/%s/modules/%s/tests'

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        test.module.course.duration -= test.duration / 60
        test.module.course.save()
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url % (self.object.module.course.id, self.object.module.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Question editing

class QuestionCreator(CreateView):
    model = Question
    success_url = 'edit_test'

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        test = get_object_or_404(Test, pk=kwargs['test_id'])
        if form.is_valid():
            question = form.save(False)
            question.test = test
            question.save()
        return redirect(self.success_url, course_id=test.module.course.id, module_id=test.module.id, test_id=test.id)
    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class QuestionUpdater(UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = '/editor/courses/%s/modules/%s/tests/%s'

    def get_success_url(self):
        return self.success_url % (self.object.test.module.course.id, self.object.test.module.id, self.object.test.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class QuestionDeleter(DeleteView):
    model = Question
    form_class = QuestionForm
    success_url = '/editor/courses/%s/modules/%s/tests/%s'

    def get_success_url(self):
        return self.success_url % (self.object.test.module.course.id, self.object.test.module.id, self.object.test.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Answer editing

class AnswerCreator(CreateView):
    model = Answer
    success_url = 'edit_test'

    def post(self, request, *args, **kwargs):
        form = AnswerForm(request.POST)
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        if form.is_valid():
            answer = form.save(False)
            answer.question = question
            answer.save()
        return redirect(
            self.success_url, course_id=question.test.module.course.id, module_id=question.test.module.id, test_id=question.test.id)
    
    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class AnswerUpdater(UpdateView):
    model = Answer
    form_class = AnswerForm
    success_url = '/editor/courses/%s/modules/%s/tests/%s'

    def get_success_url(self):
        return self.success_url % (
            self.object.question.test.module.course.id, self.object.question.test.module.id, self.object.question.test.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class AnswerDeleter(DeleteView):
    model = Answer
    form_class = AnswerForm
    success_url = '/editor/courses/%s/modules/%s/tests/%s'

    def get_success_url(self):
        return self.success_url % (
            self.object.question.test.module.course.id, self.object.question.test.module.id, self.object.question.test.id)

    @method_decorator(group_required('teachers'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#Editor views

class EditCourse(TemplateView):
    template_name = 'course_editor.html'
    form_class = CourseForm

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id'] 
        if is_not_author(request, course_id):
            return redirect('forbidden')
        form = self.get_form(course_id)
        return self.render_to_response(
            self.get_context_data(
                course_form=form, 
                course_id=course_id,
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
        course_id = kwargs['course_id'] 
        module_id = kwargs['module_id']
        test_id = kwargs['test_id']
        if is_not_author(request, course_id):
            return redirect('forbidden')
        test_form = self.get_form(test_id)
        question_forms = self.get_question_forms(test_id)

        return self.render_to_response(
            self.get_context_data(
                test_form=test_form,
                test_id=test_id,
                course_id=course_id,
                module_id=module_id,
                question_form=QuestionForm,
                answer_form=AnswerForm,
                question_forms=question_forms,
                loginpartial=login_partial(request)
            )
        )

    def get_form(self, test_id):
       test = get_object_or_404(Test, id=test_id)
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