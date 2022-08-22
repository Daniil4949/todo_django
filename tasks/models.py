from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(max_length=1000, db_index=True, null=True, blank=True, verbose_name='URL', unique=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    completed_tasks = models.IntegerField(default=0)
    uncompleted_tasks = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'



# Create your models here.
