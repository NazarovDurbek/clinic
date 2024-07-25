from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('F', 'Женщина'),
        ('M', 'Мужчина'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)