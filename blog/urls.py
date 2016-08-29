from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.post_list,name='post_list'),
	url(r'^post/new/$',views.post_new,name='post_new'),
	url(r'^drafts/$',views.post_draft_list,name='post_draft_list'),
	url(r'^post/(?P<slug>[\w-]+)/$',views.post_detail,name='post_detail'),
	url(r'^post/(?P<slug>[\w-]+)/edit/$',views.post_edit,name='post_edit'),
	url(r'^post/(?P<slug>[\w-]+)/publish/$',views.post_publish,name='post_publish'),
	url(r'^post/(?P<slug>[\w-]+)/remove/$',views.post_remove,name='post_remove'),

	url(r'^contact/$',views.contact_me,name='contact_me'),
	url(r'^profile/$',views.resume,name='resume'),
]