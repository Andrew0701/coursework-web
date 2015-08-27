from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UsersGroup
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import date
from django import template
from  .models import Group, Student, Teacher, Student_Subject, Subject, Job, Semester
import json

#making available filters in templates
register = template.Library()
	
def reg(request):
	#пользователь изменил курс (значение выпадающего списка)
	if request.is_ajax() and request.method=='GET':
		requestedYear = request.GET['year']
		groups_objects = Group.objects.filter(year=requestedYear)
		groups = [str(group) for group in groups_objects]

		return HttpResponse(json.dumps(groups), content_type='application/json' )

	#регистрация пользователя
	elif request.method=='POST':

		user = User.objects.create_user(
			request.POST['login'],
			email = request.POST['email'],
			password = request.POST['password'],
			first_name = request.POST['name'],
			last_name = request.POST['surname']
		)

		if request.POST['user_type'] == 'student':
			UsersGroup.objects.get(name='Students').user_set.add(user)

			Student.objects.create(
				user = user,
				name = request.POST['name'],
				surname = request.POST['surname'],
				patronymic = request.POST['patronymic'],
				group = Group.objects.get(name=request.POST['group'])
			)

		elif request.POST['user_type'] == 'teacher':

			UsersGroup.objects.get(name='Teachers').user_set.add(user)

			Teacher.objects.create(
				user = user,
				name = request.POST['name'],
				surname = request.POST['surname'],
				patronymic = request.POST['patronymic'],
			)

		return render(request,'home/reg-success.html')
		
	else:
		#запрос формы регистрации
		years = set( Group.objects.values_list('year',flat=True) )
		years = sorted(list(years))
		return render(request,'home/reg.html',locals())

def log_in(request):

	if request.method == 'GET':
		return render(request,'home/login.html')

	elif request.method == 'POST':

		user = authenticate(
			username=request.POST['login'],
			password=request.POST['password']
		)
		if user is not None:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('home:main'))
			else:
				return render(request, 'home/main.html', {
					'error_message':'Ваш аккаунт заблокирован'
					}
				)
		return render(request,'home/main.html',{
			'error_message':'Неверный логин или пароль'
			}
		)

def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:main'))

def main(request):
	user = request.user
	subjects = None
	jobs = list()
	currentSemesters = None

	isUserStudent = user.groups.filter(name='Students').exists()
	isUserTeacher = user.groups.filter(name='Teachers').exists()

	if isUserStudent:
		subjects = user.student.subjects.all()

	if isUserTeacher:
		subjects = set(user.teacher.subjects.all())
		currentSemesters = list( 
			filter( (lambda s : s.isCurrent()), Semester.objects.all() )
		)
		currentSubjects = set()
		for semester in currentSemesters:
			currentSubjects |= set(semester.subjects.all())

		subjects &= currentSubjects

		for subject in subjects:
			for semester in currentSemesters:
				if subject in semester.subjects.all():
					print(semester.group.name)

	if isUserStudent or isUserTeacher:
		for subject in subjects:
				for job in subject.job_set.all():
					jobs.append( job )

	if isUserStudent:
		return render(request,'home/student-main.html',locals())
	elif isUserTeacher:
		return render(request,'home/teacher-main.html',locals())
	else:
		return render(request,'home/main.html',locals())

def settings(request):

	if request.method == 'POST':

		if  request.is_ajax():

			if request.POST['action'] == 'student_add_subject':

				Student_Subject.objects.create(
					student = Student.objects.get(pk=request.POST['studentid']),
					subject = Subject.objects.get(pk=request.POST['subjectid']),
					teacher = Teacher.objects.get(pk=request.POST['teacherid'])
				)

				return HttpResponse(json.dumps(_('Предмет добавлен')), content_type='application/json')

			elif request.POST['action'] == 'student_delete_subject':

				Student_Subject.objects.get(
					student__id = request.POST['studentid'],
					subject__id = request.POST['subjectid']
				).delete()

				return HttpResponse(json.dumps(_('Предмет удален')),content_type='application/json')

			elif request.POST['action'] == 'student_change_teacher':

				try:
					studentSubjectRecord = Student_Subject.objects.get(
						student__id = request.POST['studentid'],
						subject__id = request.POST['subjectid']
					)
					studentSubjectRecord.teacher = Teacher.objects.get(pk = request.POST['teacherid'])
					studentSubjectRecord.save()

				except ObjectDoesNotExist:
					#если предмет не выбран нет смысла менять преподавателя
					pass

				return HttpResponse(json.dumps(_('Преподаватель изменен')), content_type='application/json')

			elif request.POST['action'] == 'teacher_add_subject':

				subject = Subject.objects.get(pk = request.POST['subjectid'])
				request.user.teacher.subjects.add( subject )
				request.user.teacher.save()

				return HttpResponse(json.dumps(_('Предмет добавлен')), content_type='application/json')

			elif request.POST['action'] == 'teacher_delete_subject':

				teacher = request.user.teacher
				subject = Subject.objects.get(pk = request.POST['subjectid'] )
				
				studentSubjectRecords = Student_Subject.objects.filter(
					teacher__id = teacher.id,
					subject__id = subject.id
				)

				for record in studentSubjectRecords:
					record.delete()

				teacher.subjects.remove( subject )
				teacher.save()

				return HttpResponse(json.dumps(_('Предмет удален')),content_type='application/json')

			elif request.POST['action'] == 'add_job':

				subject = Subject.objects.get(pk = request.POST['subjectid'])
				Job.objects.create(
					subject = subject,
					name = request.POST['name']
				)

				return HttpResponse(json.dumps(_('Работа добавлена')),content_type='application/json')

			elif request.POST['action'] == 'delete_job':

				Job.objects.get(pk = request.POST['jobid']).delete()

				return HttpResponse(json.dumps(_('Работа удалена')),content_type='application/json')

			elif request.POST['action'] == 'edit_job':

				job = Job.objects.get(pk = request.POST['jobid'])
				job.name = request.POST['new_name']
				job.save()

				return HttpResponse(json.dumps(_('Название изменено')),content_type='application/json')

			return HttpResponse('')

		#POST, but not ajax
		else:
			user = request.user
			if check_password(request.POST['old-password'], user.password):
				if request.POST['new-password'] == request.POST['repeat-password']:
					user.password = make_password(request.POST['new-password'])
					user.save()
					return render(request,'home/settings.html',{
							'success_message':_('Новый пароль установлен')
						}
					)
				else:
					return render(request,'home/settings.html',{
							'error_message':_('Пароли не совпадают')
						}
					)
			else:
				return render(request,'home/settings.html',{
						'error_message':_('Неверный пароль!')
					}
				)

	else:
		user = request.user

		isUserStudent = user.groups.filter(name='Students').exists()
		isUserTeacher = user.groups.filter(name='Teachers').exists()

		currentSemesters = list( 
				filter( (lambda s : s.isCurrent()), Semester.objects.all() )
			)
		currentSubjects = set()
		for semester in currentSemesters:
			currentSubjects |= set(semester.subjects.all())

		subjects = currentSubjects
			
		if isUserStudent:
			return render(request,'home/student-settings.html',locals())

		elif isUserTeacher:
			return render(request,'home/teacher-settings.html',locals())
		else:
			return render(request,'home/main.html',locals())