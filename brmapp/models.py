from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    def __str__(self):
        return self.title
class BRMuser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=30, null=False)
    def __str__(self):
        return self.nickname
