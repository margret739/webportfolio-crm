from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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