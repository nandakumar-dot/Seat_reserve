from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ManagerRegistrationSerializer,
    EmployeeRegistrationSerializer,
    LoginSerializer
)
from .models import Manager, Employee
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Seat, TimeSlot, Reservation
from .serializers import SeatSerializer, TimeSlotSerializer, ReservationSerializer


class RegisterManager(APIView):
    def post(self, request):
        serializer = ManagerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterEmployee(APIView):
    def post(self, request):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerList(APIView):
    
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        managers = Manager.objects.all()
        data = [{'manager_id': manager.id, 'username': manager.user.username, 'email': manager.user.email, 'balance': manager.balance} for manager in managers]
        return Response(data, status=status.HTTP_200_OK)


class EmployeeList(APIView):
    
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        employees = Employee.objects.all()
        data = [{'employee_id': employee.id, 'username': employee.user.username, 'email': employee.user.email, 'manager': employee.manager.user.username} for employee in employees]
        return Response(data, status=status.HTTP_200_OK)

class ManagerBalanceView(APIView):
    
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    def get(self, request, manager_id):
        try:
            manager = Manager.objects.get(id=manager_id)
            return Response({'manager_id':manager.id , 'manager_name':manager.user.username , 'balance': manager.balance}, status=status.HTTP_200_OK)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        

class SeatListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seats = Seat.objects.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

class TimeSlotListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        time_slots = TimeSlot.objects.all()
        serializer = TimeSlotSerializer(time_slots, many=True)
        return Response(serializer.data)

class MakeReservation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            seat = serializer.validated_data['seat']
            if seat.is_available:  
                seat.is_available = False
                seat.save()
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except serializer.ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Seat is not available."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
