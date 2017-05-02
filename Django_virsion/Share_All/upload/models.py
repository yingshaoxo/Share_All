from django.db import models
from django.contrib.auth.models import User as UserAccount

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=600)
    file_id = models.CharField(max_length=200)
    file_url = models.CharField(max_length=500)
