from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, AddImage


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text=""

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')



class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['tags'].required = True
        self.fields['tags'].required = False
        self.fields['telegram'].required = False
        self.fields['vk'].required = False
        self.fields['git'].required = False

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'tags', 'contact', 'vk', 'git', 'telegram']
        widgets = {
                "bio": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Описание, расскажите о себе.'
                }),
                
                "tags": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ваши умения. (Java, Дизайн, Computer Sciense)',
                }),

                "contact": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ссылка, чтобы связаться с вами'

                }),
              
                "vk": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ссылка, чтобы связаться с вами'

                }),
                
                "git": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ссылка, чтобы связаться с вами'

                }),
                
                "telegram": forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ссылка, чтобы связаться с вами'

                }),
                  
            }


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=12,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=12,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=12,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



class AddImageForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=74, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AddImage
        fields = ['title', 'image']
