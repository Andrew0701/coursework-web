from django.contrib import admin
from .models import Group, Student, Teacher, Subject, Job, Log, Student_Subject

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Job)
admin.site.register(Log)
admin.site.register(Student_Subject)
