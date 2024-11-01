from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True)
    # Other tenant-specific fields (e.g., plan, domain)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    # Other user-specific fields (e.g., email, first_name, last_name)
    
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()
    # Other transaction-specific fields (e.g., description, merchant)
    

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])