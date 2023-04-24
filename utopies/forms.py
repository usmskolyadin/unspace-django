from django import forms
from .models import Utopies, UtopiaComment
from django.forms import ModelForm, TextInput, Textarea


class UtopiesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(UtopiesForm, self).__init__(*args, **kwargs)
	        
	class Meta:
		model = Utopies
		fields = ['title', 'tags', 'full_text', 'project']

		widgets = {
			"title": TextInput(attrs={
					'class': 'form-control',
					'placeholder': 'Название утопии'
			}),

			"tags": TextInput(attrs={
					'class': 'form-control',
					'placeholder': 'Теги (дизайн, маркетинг, программирование, идея, бизнес..)',
			}),

			"project": TextInput(attrs={
					'class': 'form-control',
					'placeholder': 'Название проекта'
			}),
			

			
			"full_text": Textarea(attrs={
					'class': 'form-control',
					'placeholder': 'Расскажите о вашем проекте или идее'

			}),
			
		}



class UtopiaCommentForm(forms.ModelForm):
	class Meta:
		model = UtopiaComment
		fields = ['comment',]
		widgets = {
			"comment": TextInput(attrs={
					'class': 'form-control',
					'placeholder': 'Напишите комментарий к записи'
			}),

		}