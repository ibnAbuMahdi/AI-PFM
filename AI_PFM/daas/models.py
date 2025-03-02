from django.db import models
from tenants.models import User


class DAASUser(User):
    is_agent = models.BooleanField(default=True)
    name = models.CharField(null=True, max_length=100)
    code = models.CharField(null=True, max_length=6, unique=True)
    activated = models.BooleanField(default=False)
    
class Prospect(models.Model):
    agent = models.ForeignKey(DAASUser, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)
    name = models.TextField(null=True)
    address = models.TextField(null=True)
    message = models.TextField(blank=True, null=True)
    phone = models.CharField(null=True, max_length=15)
    school = models.TextField(null=True)
    package = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    stage = models.CharField(max_length=20, default='cont', choices=[('cont', 'Contact'), ('disc', 'Discussion'), ('app', 'Appointment'), ('dec', 'Decision'), ('agr', 'Agreement')])
    status = models.BooleanField(default=True)
    meetingdate = models.DateTimeField(null=True)
    meetinglocation = models.TextField(null=True)
# Create your models here.
