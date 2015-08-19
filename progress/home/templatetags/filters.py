from django import template
from ..models import Student_Subject

register = template.Library()

@register.filter
def teacherOf(student,subject):
	return Student_Subject.objects.get(student = student, subject = subject).teacher

@register.filter
def studentsOf(teacher,subject):
	return (item.student for item in Student_Subject.objects.filter(teacher = teacher, subject = subject))