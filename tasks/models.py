from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(max_length=1000, db_index=True, null=True, blank=True, verbose_name='URL', unique=True)

    def __str__(self):
        return f'{self.title}'



# Create your models here.
