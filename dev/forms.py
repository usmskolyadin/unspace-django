from django import forms
from .models import Startup, Team
from django.forms import ModelForm, TextInput, Textarea, URLField


class StartupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StartupForm, self).__init__(*args, **kwargs)
		self.fields['site'].required = False

	image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Startup
		fields = ['title', 'discription', 'image', 'site', 'git']

		widgets = {
		"title": forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Название проекта'
			}),

		"discription": forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Описание проекта',
			}),


		"site": forms.URLInput(attrs={
			'class': 'form-control',
			'placeholder': 'Сайт проекта (Если есть)'

			}),

		"git": forms.URLInput(attrs={
			'class': 'form-control',
			'placeholder': 'GitHub проекта'

			}),
		}

class TeamForm(forms.ModelForm):
	image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Team
		fields = ['title', 'discription', 'image']

		widgets = {
		"title": forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Название команды'
			}),

		"discription": forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Описание команды',
			}),
		}

