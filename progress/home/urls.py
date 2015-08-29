from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.main,name='main'),
	url(r'^reg/$',views.reg,name='reg'),
	url(r'^login/$',views.log_in,name='login'),
	url(r'^logout/$',views.log_out,name='logout'),
	url(r'^settings/$',views.settings,name='settings'),
	url(r'^register/' +
		'(?P<short_subject_name>[\w]+)/' +
		'(?P<group_name>.+-\d{2}\w)$',
		views.register_table, name='register'
	),
]