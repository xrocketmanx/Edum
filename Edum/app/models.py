"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    tests_results = models.ManyToManyField(
        'Test',
        through='TestResult',
        through_fields=('user','test')
    )
    signed_courses = models.ManyToManyField(
        'Course',
        through='CourseProgress',
        through_fields=('user','course'),
        related_name='signed_courses'
    )

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=250)
    duration = models.FloatField(default=0)
    overview = models.TextField()
    author = models.ForeignKey(User, related_name = 'courses', default = 0)
    rating = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class CoursesLikes(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey('Course')
    
class Module(models.Model):
    name = models.CharField(max_length=250) 
    overview = models.TextField()
    course = models.ForeignKey('Course', related_name = 'modules')

    def __str__(self):
        return self.name

class Lecture(models.Model):
    video_url = models.TextField()
    name = models.CharField(max_length=250)
    module = models.ForeignKey('Module', related_name = 'lectures')

    def __str__(self):
        return self.name

class Test(models.Model):
    module = models.ForeignKey('Module', related_name = 'tests')
    name = models.CharField(max_length=250)
    duration = models.IntegerField() # minutes
    question_count = models.IntegerField()

    def __str__(self):
        return self.name

class Question(models.Model):
    answer_count = models.IntegerField()
    text = models.TextField()
    test = models.ForeignKey('Test', related_name = 'questions')

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey('Question', related_name = 'answers')
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    test = models.ForeignKey('Test')
    user = models.ForeignKey('UserProfile')
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user.username + " " + self.test.name

class CourseProgress(models.Model):
    user = models.ForeignKey('UserProfile')
    course = models.ForeignKey('Course')
    progress = models.IntegerField(default=0) # between 0 and 100

    def __str__(self):
        return self.user.user.username + self.course.name