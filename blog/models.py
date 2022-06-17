from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    publishedDate=models.DateTimeField(blank=True,null=True)

    #methods
    def published(self):
        self.publishedDate = timezone.now()
        self.save()
    def __str__(self):
        return self.title
# Create your models here.
