from django import forms
from .models import Post

from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
	text=forms.CharField(widget=PagedownWidget())
	# published_date=forms.DateField(widget=forms.SelectDateWidget(attrs=None))
	class Meta:
		model=Post
		fields=('title','image','text','published_date',)


class ContactMe(forms.Form):
	name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'padding': '100'}))
	mobile = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
	email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
	message = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'mdl-textfield__input'}))