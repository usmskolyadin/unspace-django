# Generated by Django 4.1.7 on 2023-04-14 18:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dev', '0002_alter_team_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={},
        ),
        migrations.AddField(
            model_name='team',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]