from django.db import models
from ckeditor.fields import RichTextField
# from django.core.cache import cache


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    def __str__(self):
        return self.question