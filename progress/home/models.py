from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Subject(models.Model):
	name = models.CharField(max_length = 100)
	short_name = models.CharField(max_length = 10, unique=True, null=True)

	def __str__(self):
		return self.name

class Job(models.Model):
	name = models.CharField(max_length = 512)
	short_name = models.CharField(max_length = 10, null=True)
	subject = models.ForeignKey(Subject)

	def __str__(self):
		return self.name

class Group(models.Model):
	name = models.CharField(max_length=10)
	year = models.IntegerField()
	
	def __str__(self):
		return self.name

class Semester(models.Model):
	group = models.ForeignKey(Group)
	number = models.IntegerField(default=1)
	subjects = models.ManyToManyField(Subject)

	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)

	def isCurrent(self):
		return self.start_date <= date.today() <= self.end_date

	def __str__(self):
		return self.group.name + ' semester ' + str(self.number)

class Student(models.Model):
	user = models.OneToOneField(User,null=True)
	name = models.CharField(max_length=100)
	patronymic = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	group = models.ForeignKey(Group,null=True)

	subjects = models.ManyToManyField(Subject, through='Student_Subject')
	jobs = models.ManyToManyField(Job, through='Log')

	def __str__(self):
		return self.surname + ' ' + self.name

class Teacher(models.Model):
	user = models.OneToOneField(User,null=True)
	name = models.CharField(max_length=100)
	patronymic = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)

	subjects = models.ManyToManyField(Subject)

	def __str__(self):
		return self.surname + ' ' + self.name + ' ' + self.patronymic

class Student_Subject(models.Model):
	student = models.ForeignKey(Student)
	subject = models.ForeignKey(Subject)
	teacher = models.ForeignKey(Teacher)

	def __str__(self):
		return (
			str(self.student) + ' - ' +
			str(self.subject) + ' - ' +
			str(self.teacher.surname)
		)

class Log(models.Model):
	job = models.ForeignKey(Job)
	student = models.ForeignKey(Student)

	mark = models.IntegerField(null=True)
	date = models.DateField()
	confirmed = models.BooleanField(default=False)

	def __str__(self):
		return (
			str(self.student) + ' - ' + 
			str(self.job.subject) + ' - ' + 
			str(self.job)
		)