from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from  .models import Group
import json

# Create your views here.
def home(request):
	return render(request,'home/base.html')
	
def reg(request):
	if request.is_ajax() and request.method=='GET':
		requestedCourse = request.GET['course']
		groups_objects = Group.objects.filter(course=requestedCourse)
		groups = [str(group) for group in groups_objects]

		return HttpResponse(json.dumps(groups), content_type='application/json' )

	elif request.method=='POST':
		login = request.POST['login']
		email = request.POST['email']
		password = request.POST['password']

		user = User.objects.create_user(login,email,password)
		print("регистрация прошла успешно!")
		return HttpResponse('')
		
	else:
		courses_set = set( Group.objects.values_list('course',flat=True) )
		context = {
			'courses':sorted(list(courses_set))
		}
		return render(request,'home/reg.html',context)