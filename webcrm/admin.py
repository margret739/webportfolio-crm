from django.contrib import admin
from .models import Customer, Agent

admin.site.register(Customer)
admin.site.register(Agent)