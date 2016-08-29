from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.sitemaps import ping_google

def upload_location(instance,filename):
	return "%s/%s"%(instance.id,filename)

class Post(models.Model):
	slug=models.SlugField(unique=True)
	author=models.ForeignKey('auth.User')
	title=models.CharField(max_length=200)
	text=models.TextField()
	image=models.FileField(upload_to=upload_location,null=True,blank=True)
	created_date=models.DateTimeField(default=timezone.now)
	published_date=models.DateTimeField(default=timezone.now,blank=True,null=True)

	def save(self,*args,**kwargs):
		super(Post,self).save(*args,**kwargs)
		try:
			ping_google()
		except Exception:
			pass

	def publish(self):
		self.published_date=timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("post_detail",kwargs={"slug":self.slug})

	def get_edit_url(self):
		return reverse("post_edit",kwargs={"slug":self.slug})

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug="%s-%s"%(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver,sender=Post)