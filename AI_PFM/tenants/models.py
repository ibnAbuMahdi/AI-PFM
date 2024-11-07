from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True)
    # Other tenant-specific fields (e.g., plan, domain)
    def __str__(self):
        return self.name

class TenantBaseModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
    
    
class User(TenantBaseModel, AbstractUser):
    # Other user-specific fields (e.g., email, first_name, last_name)
    email = models.EmailField()
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    

class Budget(TenantBaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, default="None")
    title = models.CharField(max_length=50, default="Budget Title")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class Transaction(TenantBaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, default="None", null=True)
    title = models.CharField(max_length=50, default="Transaction Title")
    date = models.DateField(auto_now=True)
    description = models.TextField(null=True)
    # Other transaction-specific fields (e.g., description, merchant)
    