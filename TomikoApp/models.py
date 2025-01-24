from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=False)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.name