from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class Job(models.Model):
	name = models.CharField(max_length = 100)
	number = models.IntegerField()

	subject = models.ForeignKey(Subject)

	def __str__(self):
		return self.name

class Group(models.Model):
	group = models.CharField(max_length=5)
	course = models.IntegerField()
	
	def __str__(self):
		return self.group

class Student(models.Model):
	user = models.OneToOneField(User,null=True)
	name = models.CharField(max_length=100)
	patronymic = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	group = models.ForeignKey(Group,null=True)

	subjects = models.ManyToManyField(Subject)
	jobs = models.ManyToManyField(Job, through='Log')

	def __str__(self):
		return self.surname + ' ' + self.name

class Log(models.Model):
	job = models.ForeignKey(Job)
	student = models.ForeignKey(Student)

	mark = models.IntegerField()
	date = models.DateField()

	def __str__(slef):
		return str(student) + ' ' + str(job)

class Teacher(models.Model):
	user = models.OneToOneField(User,null=True)
	name = models.CharField(max_length=100)
	patronymic = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)

	subjects = models.ManyToManyField(Subject)

	def __str__(self):
		return self.surname + ' ' + self.name + ' ' + self.patronymic
