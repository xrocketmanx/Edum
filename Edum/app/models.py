"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tests_results = models.ManyToManyField(
        'Test',
        through="TestResult",
        through_fields=('user','test')
    )
    courses_results = models.ManyToManyField(
        'Course',
        through="CourseProgress",
        through_fields=('user','course')
    )
    signed_courses = models.ManyToManyField(
        'Course',
        related_name="signed_courses"
    )

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=250)
    overview = models.TextField()
    duration = models.IntegerField() # hours, think about this shit
    author = models.ForeignKey('UserProfile', related_name = "courses", default = 0)

    def __str__(self):
        return self.name
    
class Module(models.Model):
    test_count = models.IntegerField(default=0) # to delete
    lecture_count = models.IntegerField(default=0) # to delete
    name = models.CharField(max_length=250) 
    overview = models.TextField()
    course = models.ForeignKey('Course', related_name = "modules")

    def __str__(self):
        return self.name

class Lecture(models.Model):
    video_url = models.TextField()
    name = models.CharField(max_length=250)
    module = models.ForeignKey('Module', related_name = "lectures")

    def __str__(self):
        return self.name

class Test(models.Model):
    question_count = models.IntegerField(default=0)
    module = models.ForeignKey('Module', related_name = "tests")
    name = models.CharField(max_length=250)
    duration = models.IntegerField() # minutes

    def __str__(self):
        return self.name

class Question(models.Model):
    answer_count = models.IntegerField()
    question = models.TextField()
    test = models.ForeignKey('Test', related_name = "questions")

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey('Question', related_name = "answers")
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class TestResult(models.Model):
    test = models.ForeignKey('Test')
    user = models.ForeignKey('UserProfile')
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.login, self.test.name

class CourseProgress(models.Model):
    user = models.ForeignKey('UserProfile')
    course = models.ForeignKey('Course')
    progress = models.IntegerField(default=0) # between 0 and 100

    def __str__(self):
        return self.user.login, self.course.name