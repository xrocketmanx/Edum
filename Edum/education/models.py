"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=250)
    overview = models.TextField()
    duration = models.IntegerField() # hours

    def __str__(self):
        return self.name
    
class Module(models.Model):
    test_count = models.IntegerField(default=0) #nukk=false don needed
    lecture_count = models.IntegerField(default=0)
    name = models.CharField(max_length=250) 
    overview = models.TextField()
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    video_url = models.TextField()
    name = models.CharField(max_length=250)
    module = models.ForeignKey(Module)

    def __str__(self):
        return self.name

class Test(models.Model):
    question_count = models.IntegerField(default=0)
    module = models.ForeignKey(Module)
    name = models.CharField(max_length=250)
    duration = models.IntegerField() # minutes

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user_auth = models.OneToOneField(User)
    first_name = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    login = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    tests_results = models.ManyToManyField(
        Test,
        through="TestResult",
        through_fields=('user','test')
    )
    courses_results = models.ManyToManyField(
        Course,
        through="CourseProgress",
        through_fields=('user','course')
    )
    signed_courses = models.ManyToManyField(
        Course,
        related_name="signed_courses"
    )

    def __str__(self):
        return self.login

class Question(models.Model):
    answer_count = models.IntegerField()
    question = models.TextField()
    test = models.ForeignKey(Test)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class TestResult(models.Model):
    test = models.ForeignKey(Test)
    user = models.ForeignKey(UserProfile)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.login, self.test.name

class CourseProgress(models.Model):
    user = models.ForeignKey(UserProfile)
    course = models.ForeignKey(Course)
    progress = models.IntegerField(default=0) # between 0 and 100

    def __str__(self):
        return self.user.login, self.course.name