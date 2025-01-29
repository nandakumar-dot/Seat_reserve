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

class Seat(models.Model):
    seat_number = models.CharField(max_length=20, unique=True)  # e.g., A1, B2
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.seat_number

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class Reservation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)  
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.employee.user.username} -> {self.seat.seat_number} @ {self.time_slot}"
