from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Post

class BlogSitemap(Sitemap):
	changefreq="never"
	priority=0.5

	def items(self):
		return Post.objects.all()

	def lastmod(self,obj):
		return obj.published_date

	def location(self,obj):
		return '/post/'+str(obj.slug)