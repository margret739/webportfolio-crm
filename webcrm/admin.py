from django.contrib import admin
from .models import Customer, Agent, Product

admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(Product)