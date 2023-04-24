from django import forms
from .models import ITUtopies, ITUtopiaComment


class ITUtopiesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ITUtopiesForm, self).__init__(*args, **kwargs)
		self.fields['code'].required = False



	class Meta:
		model = ITUtopies
		fields = ['title', 'tags', 'full_text', 'code', 'project']
		widgets = {
			'project': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вашего проекта'}),
			'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш код'}),
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок вашего вопроса'}),
			'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Теги (Через запятую)'}),
			'full_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Полный текст вашей Айтопии'}),

		}

  

class ITUtopiaCommentForm(forms.ModelForm):
	class Meta:
		model = ITUtopiaComment
		fields = ('comment',)
		widgets = {
			"comment": forms.Textarea(attrs={
					'class': 'form-control',
					'placeholder': 'Напишите комментарий к записи'
			}),

		}