from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.utils import timezone
import uuid
from uuid import uuid4
from pytils.translit import slugify
 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_avatars')
    bio = models.CharField(max_length=100, validators=[MinLengthValidator(50)],  blank=True, default='Добро пожаловать на UnrealSpace! Пожалуйста, заполните свой профиль. ')
    tags = TaggableManager()
    contact = models.URLField(default="http://")
    date_registered = models.DateTimeField(auto_now_add=True)
    raiting = models.ManyToManyField(User, related_name='raiting')
    slug = models.SlugField(max_length=255, default=uuid.uuid4,
                            allow_unicode=True, db_index=True, verbose_name="URL")
    verify = models.BooleanField('Галочка', default=False)
    telegram = models.URLField('Телеграм пользователя')
    vk = models.URLField('Вконтакте пользователя')
    git = models.URLField('GitHub пользователя')

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('account', kwargs=kwargs)


    def total_raiting(self):
        return self.raiting.count()

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id
        }
        return reverse('profile', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.user.username
        self.slug = slugify(value)
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 180 or img.width > 180:
            output_size = (180,180)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class AddImage(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField('Фото', upload_to="profile_images")
    title = models.CharField('Заголовок', max_length=69)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('profile')

    def save(self, *args, **kwargs):
        super(AddImage, self).save(*args, **kwargs)

        image = Image.open(self.image.path)

        if image.height > 4000 or image.width > 4000:
            output_size = (4000,4000)
            image.thumbnail(output_size)
            image.save(self.image.path)

    class Meta:
        verbose_name = 'Картинка пользователя'
        verbose_name_plural = 'Картинки пользователей'

