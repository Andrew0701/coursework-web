from django import template
from ..models import Student_Subject, Subject, Log
from django.utils.translation import ugettext as _

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

@register.filter
def get_days_plural(days):
	if days % 10 == 0 or days in range(10,20):
		return _('дней')
	elif days % 10 == 1:
		return _('день')
	elif days % 10 in [2,3,4]:
		return _('дня')
	else:
		return _('дней')

@register.filter
def get_weeks_plural(weeks):
	if weeks % 10 == 0 or weeks in range(10,20):
		return _('недель')
	elif weeks % 10 == 1:
		return _('неделя')
	elif weeks % 10 in [2,3,4]:
		return _('недели')
	else:
		return _('недель')