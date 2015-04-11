
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import *

class CourseForm(ModelForm):
    
    class Meta:
        model = Course
        fields = ['name', 'overview', 'duration']

class ModuleForm(ModelForm):
    
    class Meta:
        model = Module
        fields = ['name', 'overview']

class LectureForm(ModelForm):
    
    class Meta:
        model = Lecture
        fields = ['name', 'video_url']
