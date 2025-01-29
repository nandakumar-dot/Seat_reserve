from django.urls import path
from .views import RegisterManager, RegisterEmployee, Login, ManagerList, EmployeeList, ManagerBalanceView
from .views import SeatListView, TimeSlotListView, MakeReservation, SeatAvailabilityView, ManagerBookings, EmployeeBookings, ManagerInfo, EmployeeInfo, ValidateToken

urlpatterns = [
    path('register/manager/', RegisterManager.as_view(), name='register_manager'),
    path('register/employee/', RegisterEmployee.as_view(), name='register_employee'),
    path('login/', Login.as_view(), name='login'),
    path('managers/', ManagerList.as_view(), name='manager_list'),
    path('employees/', EmployeeList.as_view(), name='employee_list'),
    path('manager/<int:manager_id>/balance/', ManagerBalanceView.as_view(), name='manager-balance'),
    path('seats/', SeatListView.as_view(), name='seat-list'),
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
    path('make-reservation/', MakeReservation.as_view(), name='make-reservation'),
    path('seats/status/<int:time_slot_id>/', SeatAvailabilityView.as_view(), name='seat_availability'),
    path('manager/<int:manager_id>/bookings/', ManagerBookings.as_view(), name='manager-bookings'),
    path('employee/<int:employee_id>/bookings/', EmployeeBookings.as_view(), name='employee-bookings'),
    path('manager/<int:manager_id>/info/', ManagerInfo.as_view(), name='manager-info'),
    path('employee/<int:employee_id>/info/', EmployeeInfo.as_view(), name='employee-info'),
    path('auth/validate-token/', ValidateToken.as_view(), name='validate-token')
]
