from django.db import models

# Create your models here.
class FileModel(models.Model):
    owner = models.CharField(max_length=30)
    file_id = models.CharField(max_length = 130)
    name = models.CharField(max_length = 100)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now=True)
