from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True, db_index=True)


    class Meta:
        db_table = 'usermanagement'

class Company(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    industry = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    employees = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name