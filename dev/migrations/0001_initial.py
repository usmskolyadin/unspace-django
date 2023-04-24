# Generated by Django 4.1.7 on 2023-04-14 06:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Название команды')),
                ('discription', models.CharField(max_length=71, validators=[django.core.validators.MinLengthValidator(50)], verbose_name='Описание')),
                ('image', models.ImageField(upload_to='teampics', verbose_name='Обложка команды')),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Стартап',
                'verbose_name_plural': 'Стартапы',
            },
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, default=uuid.uuid4, max_length=255, verbose_name='URL')),
                ('title', models.CharField(max_length=25, verbose_name='Название проекта')),
                ('discription', models.CharField(max_length=71, validators=[django.core.validators.MinLengthValidator(50)], verbose_name='Описание')),
                ('image', models.ImageField(upload_to='proectpics', verbose_name='Обложка проекта')),
                ('site', models.URLField(verbose_name='Сайт проекта')),
                ('git', models.URLField(verbose_name='Git проекта')),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dev.team')),
            ],
            options={
                'verbose_name': 'Стартап',
                'verbose_name_plural': 'Стартапы',
            },
        ),
    ]