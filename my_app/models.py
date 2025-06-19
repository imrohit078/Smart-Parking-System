from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

VEHICLE_TYPE_CHOICES = [
    ('Car', 'Car'),
    ('Bike', 'Bike'),
    ('Bus', 'Bus'),
]

class PlateSession(models.Model):
    plate_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    charge = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle_type})"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=50, default="Staff")  # or Manager, Gatekeeper, etc.

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"
    

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=100, default="Staff")
    is_employee = models.BooleanField(default=True)  # ✅ Add this

    def __str__(self):
        return self.user.username
    
# class EmployeeProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_employee = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username
