
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import *

class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'overview']

class ModuleForm(ModelForm):
    
    class Meta:
        model = Module
        fields = ['name', 'overview']

class LectureForm(ModelForm):
    
    class Meta:
        model = Lecture
        fields = ['name', 'video_url']

class TestForm(ModelForm):
    
    class Meta:
        model = Test
        fields = ['name', 'question_count', 'duration']

class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['question', 'answer_count']

class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['answer', 'correct']