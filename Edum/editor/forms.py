
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import *

class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'overview']
        widgets = {
            'overview': Textarea(attrs={'rows': 10, 'class': 'wide-textarea'})
        }

class ModuleForm(ModelForm):
    
    class Meta:
        model = Module
        fields = ['name', 'overview']
        widgets = {
            'overview': Textarea(attrs={'rows': 10, 'class': 'wide-textarea'})
        }

class LectureForm(ModelForm):
    
    class Meta:
        model = Lecture
        fields = ['name', 'video_url']
        widgets = {
            'video_url': Textarea(attrs={'rows': 1, 'cols': 100})
        }

    def save(self, commit = True):
        lecture = super(LectureForm, self).save(commit=False)
        url = self.cleaned_data['video_url']
        video_code = url[url.find('=') + 1:]
        embed_url = 'https://www.youtube.com/embed/' + video_code
        lecture.video_url = embed_url
        if commit:
            lecture.save()
        return lecture

class TestForm(ModelForm):
    
    class Meta:
        model = Test
        fields = ['name', 'duration', 'question_count']

class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['text', 'answer_count']
        labels = {
            'text': _('Question')
        }

class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'correct']
        labels = {
            'text': _('Answer')
        }