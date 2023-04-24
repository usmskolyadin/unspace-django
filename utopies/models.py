from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.urls import reverse
from pytils.translit import slugify
from django.contrib.auth import get_user_model
import uuid
from uuid import uuid4
from django.contrib.auth.models import User


class Utopies(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    title = models.CharField('Название', max_length=35)
    anons = models.CharField('Анонс', max_length=25)
    tags = TaggableManager()
    slug = models.SlugField(max_length=255, default=uuid.uuid4,
                            allow_unicode=True, db_index=True, verbose_name="URL", unique=True)
    full_text = models.TextField('Утопия', max_length=2000, validators=[
                                 MinLengthValidator(150)])
    date = models.DateTimeField(default=timezone.now)
    project = models.CharField('Проект', max_length=20, validators=[
                               MinLengthValidator(2)])
    contactproject = models.URLField('Ссылка на ваш проект', default="http://")
    likes = models.ManyToManyField(User, related_name='like')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('utopia', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Утопия'
        verbose_name_plural = 'Утопии'


class UtopiaComment(models.Model):
    utopia = models.ForeignKey(
        Utopies, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, validators=[
                               MinLengthValidator(10)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Комментировано {} в {}'.format(self.author, self.utopia)
