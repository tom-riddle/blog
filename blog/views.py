from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.http import  HttpResponse

from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm,ContactMe

def post_list(request):
	all_posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	
	query=request.GET.get('q')
	if query:
		all_posts=all_posts.filter(
			Q(title__icontains=query)|
			Q(text__icontains=query)
			).distinct()

	paginator=Paginator(all_posts,20)
	page=request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		posts=paginator.page(1)
	except EmptyPage:
		posts=paginator.page(paginator.num_pages)

	return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,slug):
	post=get_object_or_404(Post,slug=slug)
	return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
	if request.method=="POST":
		form=PostForm(request.POST,request.FILES)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return redirect('post_detail',slug=post.slug)
	else:
		form=PostForm()
	return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request,slug):
	post=get_object_or_404(Post,slug=slug)
	if request.method=="POST":
		form=PostForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return redirect('post_detail',slug=post.slug)
	else:
		form=PostForm(instance=post)
	return render(request,'blog/post_edit.html',{'form':form})


@login_required
def post_draft_list(request):
	posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request,'blog/post_draft_list.html',{'posts':posts})


@login_required
def post_publish(request,slug):
	post=get_object_or_404(Post,slug=slug)
	post.publish()
	return redirect('post_detail',slug=post.slug)

@login_required
def post_remove(request,slug):
	post=get_object_or_404(Post,slug=slug)
	post.delete()
	return redirect('post_list')

def contact_me(request):
	if request.method == 'POST':
		form = ContactMe(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			mobile = form.cleaned_data['mobile']
			email = form.cleaned_data['email']
			message = form.cleaned_data['message']

			recipients = ['anuragupadhyaya5@gmail.com']

			msg = 'Name : ' + name + '\n\nMobile : ' + str(mobile) + '\n\nEmail : ' + str(email) + '\n\nMessage :\n\n' + message 

			send_mail('New Hire Request', msg, 'anuragupadhyaya5@gmail.com', recipients)

			return HttpResponse('Successful Submission')

	else:
		form = ContactMe()

	return render(request, 'blog/contact_me.html', {'form': form.as_p()})


def resume(request):
    return render(request,'blog/resume.html',{})