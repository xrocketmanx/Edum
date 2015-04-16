from django import forms
from django.forms import ModelForm
from app.models import *

class CourseForm(ModelForm):
    
    class Meta:
        model = Course
        fields = ['name', 'overview', 'duration']

