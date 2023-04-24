from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from PIL import Image


class GlavProfile(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE, default='1')
	title = models.CharField('Мини-тайтл', max_length=53, validators=[MinLengthValidator(40)], default='Пример профиля, который ты получишь после регистрации')


class News(models.Model):
    image = models.ImageField('Фото', upload_to="unews_images")
    fullest = models.TextField('Новость', max_length=90)
    title = models.CharField('Заголовок', max_length=26)

    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)

        image = Image.open(self.image.path)

        if image.height > 3540 or image.width > 3540:
            output_size = (3540,3540)
            image.thumbnail(output_size)
            image.save(self.image.path)
