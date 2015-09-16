from django import template
from ..models import Student_Subject, Subject, Log

register = template.Library()

@register.filter
def teacherOf(student,subject):
	return Student_Subject.objects.get(student = student, subject = subject).teacher

@register.filter
def studentsOf(teacher,subject):
	return (item.student for item in Student_Subject.objects.filter(teacher = teacher, subject = subject))

@register.filter
def isStudent(user):
	return hasattr(user,'student')

@register.filter
def isTeacher(user):
	return hasattr(user,'teacher')

@register.filter
def teaches(teacher,student):
	return Student_Subject.objects.filter(teacher = teacher, student = student)

@register.filter
def split_by_row(string):
	return string.strip().replace(' ','<br>')

@register.filter
def log_entry_confirmed(student,job):
	log_query_set = Log.objects.filter(student = student, job = job)
	return False if not log_query_set.exists() else log_query_set[0].confirmed

@register.filter
def log_entry_mark(student,job):
	log_query_set = Log.objects.filter(student = student, job = job)
	return None if not log_query_set.exists() else log_query_set[0].mark

@register.filter
def log_entry_date(student,job):
	log_query_set = Log.objects.filter(student = student, job = job)
	return None if not log_query_set.exists() else log_query_set[0].date.strftime("%Y-%m-%d")

@register.filter
def passed(student,job):
	return Log.objects.filter(student=student, job=job).exists()