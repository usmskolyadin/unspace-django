from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.validators import MinLengthValidator
from pytils.translit import slugify
from django.contrib.auth import get_user_model
import uuid
from uuid import uuid4
from django.urls import reverse
from PIL import Image
from markdown import markdown


User = settings.AUTH_USER_MODEL

class ITUtopies(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField('Название', max_length=30)
    tags = TaggableManager('Теги')
    full_text = models.TextField('Айтиутопия', max_length=2000, validators=[MinLengthValidator(100)])
    code = models.TextField('Код')
    date = models.DateTimeField(auto_now_add=True)
    project = models.TextField('Проект', max_length=20)
    slug = models.SlugField(max_length=255, default=uuid.uuid4, allow_unicode=True, db_index=True, verbose_name="URL")
    likes = models.ManyToManyField(User, related_name='itlike')
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('itopia', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.html = markdown(self.full_text)
        self.html = markdown(self.code)
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Айтиутопия'
        verbose_name_plural = 'Айтиутопии'

class ITUtopiaComment(models.Model):
    itopia = models.ForeignKey(ITUtopies, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.CharField(max_length=150, validators=[MinLengthValidator(10)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return 'Комментировано {} в {}'.format(self.author, self.itopia)