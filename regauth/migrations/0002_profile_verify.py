# Generated by Django 4.1.7 on 2023-04-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verify',
            field=models.BooleanField(default=1, verbose_name='Галочка'),
            preserve_default=False,
        ),
    ]