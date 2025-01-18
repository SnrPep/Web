
# Create your models here.
from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.name