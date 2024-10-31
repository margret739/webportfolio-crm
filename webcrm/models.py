from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    assigned_town = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")


class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    agent = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
