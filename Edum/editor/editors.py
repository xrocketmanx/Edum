from app.models import *
from editor.forms import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class Editor(object):
    def __init__(self, ModelClass, FormClass):
        self.FormClass = FormClass
        self.ModelClass = ModelClass

    def create(self, post, **kwargs):
        form = self.get_form(post)
        model = form.save(False)
        self.update_model(model, kwargs)
        model.save()
        return model

    def update(self, post, pk):
        form = self.get_form(post)
        model = self.get_model(pk)
        self.update_model(model, form.cleaned_data)
        model.save()

    def delete(self, pk):
        model = self.get_model(pk)  
        model.delete()

    def get_model(self, pk):
        return get_object_or_404(self.ModelClass, pk=pk)  

    def get_form(self, post):
        form = self.FormClass(post)
        if not form.is_valid():
            raise ValidationError("Form validation failed!")
        return form

    def update_model(self, model, data):
        for attr in data:
            setattr(model, attr, data[attr])

course_editor = Editor(Course, CourseForm)
module_editor = Editor(Module, ModuleForm)
lecture_editor = Editor(Lecture, LectureForm)
test_editor = Editor(Test, TestForm)
question_editor = Editor(Question, QuestionForm)
answer_editor = Editor(Answer, AnswerForm)