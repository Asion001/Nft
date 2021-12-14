from django.conf import settings
from django.db import models
from django.utils import timezone


class Token(models.Model):
    owner = models.CharField(max_length=200)
    token_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title
