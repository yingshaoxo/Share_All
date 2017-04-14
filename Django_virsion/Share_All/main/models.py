from django.db import models

from django.contrib.auth.models import User as UserAccount

# Create your models here.
class Data(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
