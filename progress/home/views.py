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
from  .models import Group, Student, Teacher, \
					Student_Subject, Subject, Job, Semester, Log
import json

#making available filters in templates
register = template.Library()

def get_current_semesters():
	return list(
			filter(
				(lambda s : s.isCurrent()),
				Semester.objects.all()
			))

def get_subjects_of(semesters):
	subjects = set()
	for semester in semesters:
		subjects |= set(semester.subjects.all())
	return subjects

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
	passedJobsIds = None

	isUserStudent = hasattr(user,'student')
	isUserTeacher = hasattr(user,'teacher')

	if isUserStudent:
		subjects = user.student.subjects.all()
		passedJobsIds = [log.job.id for log in Log.objects.filter(student = user.student)]

	if isUserTeacher:
		subjects = set(user.teacher.subjects.all())
		currentSemesters = get_current_semesters()
		currentSubjects = get_subjects_of(currentSemesters)

		subjects &= currentSubjects

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

	isUserStudent = hasattr(request.user,'student')
	isUserTeacher = hasattr(request.user,'teacher')

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
					name = request.POST['name'],
					short_name = request.POST['short_name']
				)

				return HttpResponse(json.dumps(_('Работа добавлена')),content_type='application/json')

			elif request.POST['action'] == 'delete_job':

				Job.objects.get(pk = request.POST['jobid']).delete()

				return HttpResponse(json.dumps(_('Работа удалена')),content_type='application/json')

			elif request.POST['action'] == 'edit_job_name':

				job = Job.objects.get(pk = request.POST['jobid'])
				job.name = request.POST['new_name']
				job.save()

				return HttpResponse(json.dumps(_('Название изменено')),content_type='application/json')

			elif request.POST['action'] == 'edit_job_short_name':

				job = Job.objects.get(pk = request.POST['jobid'])
				job.short_name = request.POST['new_short_name']
				job.save()

				return HttpResponse(json.dumps(_('Краткое название изменено')),content_type='application/json')

			elif request.POST['action'] == 'add_log_entry':

				studentid = request.POST['studentid']
				jobid = request.POST['jobid']

				log_query_set = Log.objects.filter(student__id = studentid, job__id = jobid)
				log_entry = log_query_set[0] if log_query_set.exists() else None

				if isUserStudent:
					if not log_entry:
						Log.objects.create(
							student = request.user.student,
							job = Job.objects.get(pk = jobid),
							date = date.today(),
							confirmed = False
						)
						return HttpResponse(json.dumps(_('Запись добавлена')),content_type='application/json')

				elif isUserTeacher:
					if log_entry:
						log_entry.confirmed = True
						log_entry.save()
						return HttpResponse(json.dumps(_('Запись подтверждена')),content_type='application/json')
					else:
						Log.objects.create(
							student = Student.objects.get(pk=studentid),
							job = Job.objects.get(pk = jobid),
							date = date.today(),
							confirmed = True
						)
						return HttpResponse(json.dumps(_('Запись добавлена')),content_type='application/json')

				return HttpResponse('')

			elif request.POST['action'] == 'delete_log_entry':

				studentid = request.POST['studentid']
				jobid = request.POST['jobid']

				log_query_set = Log.objects.filter(student__id = studentid, job__id = jobid)
				log_entry = log_query_set[0] if log_query_set.exists() else None

				if isUserStudent:
					if log_entry:
						if not log_entry.confirmed:
							log_entry.delete()
							return HttpResponse(json.dumps(_('Запись удалена')),content_type='application/json')

				elif isUserTeacher:
					if log_entry:
						log_entry.confirmed = False
						log_entry.save()
						return HttpResponse(json.dumps(_('Запись удалена')),content_type='application/json')

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

		isUserStudent = hasattr(user,'student')
		isUserTeacher = hasattr(user,'teacher')

		currentSemesters = get_current_semesters()
		currentSubjects = get_subjects_of(currentSemesters)

		subjects = currentSubjects
			
		if isUserStudent:
			return render(request,'home/student-settings.html',locals())

		elif isUserTeacher:
			return render(request,'home/teacher-settings.html',locals())
		else:
			return render(request,'home/main.html',locals())

def register_table(request, short_subject_name, group_name):
	subject = Subject.objects.filter(short_name = short_subject_name)
	group = Group.objects.filter(name = group_name)
	semester = None

	error_message = ''
	
	current_semesters = get_current_semesters()
	current_subjects = get_subjects_of(current_semesters)

	subject = subject[0] if subject.exists() else None
	group = group[0] if group.exists() else None

	if not subject:
		error_message = _('Такого предмета нет')
	elif subject not in current_subjects:
		error_message = _('Этот предмет не актуален в текущем семестре')
	elif not group:
		error_message = _('Такой группы нет')
	elif subject not in get_subjects_of(group.semester_set.all()):
		error_message = _('Эта группа не изучает данный предмет')

	return render(request,'home/register.html',locals())