from django.urls import path
from .views import RegisterManager, RegisterEmployee, Login, ManagerList, EmployeeList, ManagerBalanceView
from .views import SeatListView, TimeSlotListView, MakeReservation

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
]
