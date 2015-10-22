from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UsersGroup
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import *
from datetime import date, timedelta
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

def get_current_semester_for(student):
	current_semester = list(
		filter(
			lambda s : s.group == student.group,
			get_current_semesters()
		)
	)
	return current_semester[0] if current_semester else None

def get_subjects_of(semesters):
	subjects = set()
	for semester in semesters:
		subjects |= set(semester.subjects.all())
	return subjects

def how_much_passed(student,semester,week_num):
	week = timedelta(weeks = 1)
	logs = Log.objects.filter(
		student = student,
		date__gte = semester.start_date + (week * week_num) - week,
		date__lt = semester.start_date + (week * week_num)
	)
	return logs.count()

def weeks_in(semester):
	return (semester.end_date - semester.start_date).days // 7

def current_week_of(semester):
	elapsed_days = (date.today() - semester.start_date).days
	elapsed_weeks = elapsed_days // 7
	return elapsed_weeks + 1

def make_plan(jobs_total_count, semester, weeks_statistics):
	next_week_num = current_week_of(semester) + 1
	jobs_left = jobs_total_count - sum(weeks_statistics)
	days_left = (semester.end_date - date.today()).days
	weeks_left = weeks_in(semester) - current_week_of(semester)
	per_week = jobs_left // weeks_left

	plan = list()
	for week_num in range(1,weeks_in(semester)+1):
		if week_num < next_week_num:
			plan.append( None )
		else:
			plan.append( per_week )

	first_step_sum = sum(map(lambda x : 0 if x is None else x,plan))
	diff = jobs_left - first_step_sum
	
	week_num = next_week_num - 1
	while diff > 0:
		plan[week_num] += 1
		diff -= 1
		week_num += 1

	#connection of lines
	current_week = current_week_of(semester)
	plan[current_week-1] = weeks_statistics[current_week-1]

	return plan 

def reg(request):
	#пользователь изменил курс (значение выпадающего списка)
	if request.is_ajax() and request.method=='GET':
		requested_year = request.GET['year']
		groups_objects = Group.objects.filter(year = requested_year)
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

		return render(request,'home/reg/success.html')
		
	else:
		#запрос формы регистрации
		years = set( Group.objects.values_list('year',flat=True) )
		years = sorted(list(years))
		return render(request,'home/reg/base.html',locals())

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
				return render(request, 'home/main/base.html', {
					'error_message':'Ваш аккаунт заблокирован'
					}
				)
		return render(request,'home/main/base.html',{
			'error_message':'Неверный логин или пароль'
			}
		)

def log_out(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect(reverse('home:main'))

def main(request):
	user = request.user
	subjects = None
	jobs = list()
	current_semesters = None
	passed_jobs_ids = None

	user_is_student = hasattr(user,'student')
	user_is_teacher = hasattr(user,'teacher')

	if user_is_student:
		subjects = user.student.subjects.all()
		passed_jobs_ids = [log.job.id for log in Log.objects.filter(student = user.student)]

	if user_is_teacher:
		subjects = set(user.teacher.subjects.all())
		current_semesters = get_current_semesters()
		current_subjects = get_subjects_of(current_semesters)

		subjects &= current_subjects

	if user_is_student or user_is_teacher:
		for subject in subjects:
				for job in subject.job_set.all():
					jobs.append( job )

	if user_is_student:
		return render(request,'home/main/student.html',locals())
	elif user_is_teacher:
		return render(request,'home/main/teacher.html',locals())
	else:
		return render(request,'home/main/base.html',locals())

def settings(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('home:main'))

	user_is_student = hasattr(request.user,'student')
	user_is_teacher = hasattr(request.user,'teacher')

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
					student_subject_record = Student_Subject.objects.get(
						student__id = request.POST['studentid'],
						subject__id = request.POST['subjectid']
					)
					student_subject_record.teacher = Teacher.objects.get(pk = request.POST['teacherid'])
					student_subject_record.save()

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
				
				student_subject_records = Student_Subject.objects.filter(
					teacher__id = teacher.id,
					subject__id = subject.id
				)

				for record in student_subject_records:
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

				if user_is_student:
					if not log_entry:
						Log.objects.create(
							student = request.user.student,
							job = Job.objects.get(pk = jobid),
							date = date.today(),
							confirmed = False
						)
						return HttpResponse(json.dumps(_('Запись добавлена')),content_type='application/json')

				elif user_is_teacher:
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

				if user_is_student:
					if log_entry:
						if not log_entry.confirmed:
							log_entry.delete()
							return HttpResponse(json.dumps(_('Запись удалена')),content_type='application/json')

				elif user_is_teacher:
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
					return render(request,'home/settings/base.html',{
							'success_message':_('Новый пароль установлен')
						}
					)
				else:
					return render(request,'home/settings/base.html',{
							'error_message':_('Пароли не совпадают')
						}
					)
			else:
				return render(request,'home/settings/base.html',{
						'error_message':_('Неверный пароль!')
					}
				)

	else:
		user = request.user

		user_is_student = hasattr(user,'student')
		user_is_teacher = hasattr(user,'teacher')

		current_semesters = get_current_semesters()
		current_subjects = get_subjects_of(current_semesters)

		subjects = current_subjects
			
		if user_is_student:
			return render(request,'home/settings/student.html',locals())

		elif user_is_teacher:
			return render(request,'home/settings/teacher.html',locals())
		else:
			return render(request,'home/main/base.html',locals())

def register_table(request, short_subject_name, group_name):

	if request.user.is_authenticated:

		if request.is_ajax():
			if request.POST['action'] == 'change_mark':
				log_entry = Log.objects.get(
					student__id = request.POST['student_id'],
					job__id = request.POST['job_id']
				)
				if request.POST['new_mark']:
					log_entry.mark = int(request.POST['new_mark'])
					log_entry.save()

				return HttpResponse(json.dumps(_('Оценка изменена')),content_type='application/json')

			if request.POST['action'] == 'change_date':
				log_entry = Log.objects.get(
					student__id = request.POST['student_id'],
					job__id = request.POST['job_id']
				)
				print(log_entry.date)

				log_entry.date = date(
					year = int(request.POST['year']),
					month = int(request.POST['month']),
					day = int(request.POST['day'])
				)
				log_entry.save()

				return HttpResponse(json.dumps(_('Дата изменена')),content_type='application/json')

		else:
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

	else:
		return HttpResponseRedirect(reverse('home:main'))

def statistics(request,student_id):

	student = get_object_or_404(Student, pk = student_id)
	current_semester = get_current_semester_for(student)
	days_left = (current_semester.end_date - date.today()).days
	weeks_left = weeks_in(current_semester) - current_week_of(current_semester)

	jobs_passed_count = student.jobs.count()
	jobs_total_count = sum( subject.job_set.count() for subject in student.subjects.all() )
	jobs_passed_percents = '%.2f' % (jobs_passed_count/jobs_total_count * 100) if jobs_total_count != 0 else 0
	jobs_left = jobs_total_count - jobs_passed_count

	if request.is_ajax():

		weeks_in_current_semester = weeks_in(current_semester)

		labels = list(range(1,weeks_in_current_semester+1))
		weeks_statistics = list()

		for week_num in range(1,weeks_in_current_semester+1):
			if week_num <= current_week_of(current_semester):
				weeks_statistics.append( how_much_passed(student,current_semester,week_num) )

		plan = make_plan(jobs_total_count, current_semester, weeks_statistics)

		data = {
			'labels' : labels,
			'dataset' : weeks_statistics,
			'plan' : plan
		}

		return HttpResponse(json.dumps(data), content_type='application/json')
	
	

	return render(request,'home/statistics.html',locals())
