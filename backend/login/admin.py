from django.contrib import admin
from .models import Employee,Manager,Seat,TimeSlot,Reservation,SeatAvailability

# Register your models here.

admin.site.register(Employee)
admin.site.register(Manager)
admin.site.register(Seat)
admin.site.register(TimeSlot)
admin.site.register(Reservation)
admin.site.register(SeatAvailability)


