from django.contrib import admin
from app.models import UserProfile, Course, Module, Lecture, Test, Question, Answer, CourseProgress, TestResult
from usersys.models import ConfirmationToken

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CourseProgress)
admin.site.register(TestResult)
admin.site.register(ConfirmationToken)