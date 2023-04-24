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
from PIL import Image
from django.utils import timezone


class Team(models.Model):
	founder = models.ForeignKey(User, on_delete=models.PROTECT)
	title = models.CharField('Название команды', max_length=25)
	discription = models.CharField('Описание', max_length=71, validators=[MinLengthValidator(50)])
	image = models.ImageField('Обложка команды', upload_to="teampics")
	participants = models.ManyToManyField(User, related_name='participants', blank=True)
	verify = models.BooleanField('Галочка', default=False)
	date = models.DateTimeField(default=timezone.now)


	def total_participants(self):
		return self.participants.count()

	def __str__(self):
		return self.title

		
	def get_absolute_url(self):
		kwargs = {
			'pk': self.id,
		}
		return reverse('team', kwargs=kwargs)

	def save(self, *args, **kwargs):
		super(Team, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	class Meta:
		verbose_name = 'Команда'
		verbose_name_plural = 'Команды'


class Startup(models.Model):
	team = models.ForeignKey(Team, on_delete=models.PROTECT)
	founder = models.ForeignKey(User, on_delete=models.PROTECT)
	slug = models.SlugField(max_length=255, default=uuid.uuid4, allow_unicode=True, db_index=True, verbose_name="URL")
	title = models.CharField('Название проекта', max_length=25)
	discription = models.CharField('Описание', max_length=71, validators=[MinLengthValidator(50)])
	image = models.ImageField('Обложка проекта', upload_to="proectpics")
	site = models.URLField('Сайт проекта')
	git = models.URLField('Git проекта')
	verify = models.BooleanField('Галочка', default=False)
	date = models.DateTimeField(default=timezone.now)


	def get_absolute_url(self):
		kwargs = {
		'pk': self.id,
		'slug': self.slug
		}
		return reverse('startup', kwargs=kwargs)

	def save(self, *args, **kwargs):
		value = self.title
		self.slug = slugify(value)
		super(Startup, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Стартап'
		verbose_name_plural = 'Стартапы'

