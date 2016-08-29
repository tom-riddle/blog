from django.contrib import admin
from django.db import models
from .models import Post
from pagedown.widgets import AdminPagedownWidget

class PostModelAdmin(admin.ModelAdmin):
	list_display=["title","created_date","published_date"]
	list_editable=["title"]

	search_fields=["title","text"]
	formfield_overrides={
		models.TextField:{'widget':AdminPagedownWidget},
	}
	class Meta:
		model=Post

admin.site.register(Post,PostModelAdmin)