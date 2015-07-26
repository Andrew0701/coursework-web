from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UsersGroup
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from  .models import Group, Student, Teacher
import json

# Create your views here.
def main(request):
	return render(request,'home/main.html',locals())
	
def reg(request):
	#пользователь изменил курс (значение выпадающего списка)
	if request.is_ajax() and request.method=='GET':
		requestedCourse = request.GET['course']
		groups_objects = Group.objects.filter(course=requestedCourse)
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
				group = Group.objects.get(group=request.POST['group'])
			)

		elif request.POST['user_type'] == 'teacher':

			UsersGroup.objects.get(name='Teachers').user_set.add(user)

			Teacher.objects.create(
				user = user,
				name = request.POST['name'],
				surname = request.POST['surname'],
				patronymic = request.POST['patronymic']
			)

		return render(request,'home/reg-success.html')
		
	else:
		#запрос формы регистрации
		courses_set = set( Group.objects.values_list('course',flat=True) )
		context = {
			'courses':sorted(list(courses_set))
		}
		return render(request,'home/reg.html',context)

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