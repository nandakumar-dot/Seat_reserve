from django.contrib.auth.models import User
from django.db import models


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    manager = models.ForeignKey(Manager, related_name='employees', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
