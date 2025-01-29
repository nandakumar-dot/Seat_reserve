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
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Seat, TimeSlot, Reservation
from rest_framework.authtoken.models import Token
from .serializers import SeatSerializer, TimeSlotSerializer, ReservationSerializer, SeatAvailability, EmployeeSerializer, ManagerSerializer


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
            time_slot = serializer.validated_data['time_slot']
            employee = serializer.validated_data['employee']
            manager = employee.manager  

            if not Reservation.is_seat_available(seat, time_slot):
                return Response({"error": "Seat is not available for this time slot."}, status=status.HTTP_400_BAD_REQUEST)

            
            if manager.balance < 10:
                return Response({"error": "Manager does not have enough balance for reservation."}, status=status.HTTP_400_BAD_REQUEST)

            
            manager.balance -= 10
            manager.save()

            
            try:
                serializer.save(manager=manager)
                
                
                seat_availability, created = SeatAvailability.objects.get_or_create(seat=seat, time_slot=time_slot)
                seat_availability.is_available = False
                seat_availability.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializer.ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeatAvailabilityView(APIView):
    def get(self, request, time_slot_id):
        try:
            time_slot = TimeSlot.objects.get(id=time_slot_id)
        except TimeSlot.DoesNotExist:
            return Response({"detail": "Time slot not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all seats
        seats = Seat.objects.all()
        seat_availability_data = []

        
        for seat in seats:
            
            seat_availability = SeatAvailability.objects.filter(seat=seat, time_slot=time_slot).first()

            if seat_availability:
                
                seat_availability_data.append({
                    'seat': seat.id,
                    'seat_number': seat.seat_number,
                    'is_available': seat_availability.is_available
                })
            else:
                
                seat_availability_data.append({
                    'seat': seat.id,
                    'seat_number': seat.seat_number,
                    'is_available': True
                })

        return Response(seat_availability_data, status=status.HTTP_200_OK)
    

class ManagerBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, manager_id):
        try:
            
            manager = Manager.objects.get(id=manager_id)
        except Manager.DoesNotExist:
            return Response({"error": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        
        reservations = Reservation.objects.filter(manager=manager)

        
        serializer = ReservationSerializer(reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        try:
            
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        
        reservations = Reservation.objects.filter(employee=employee)

        
        serializer = ReservationSerializer(reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ManagerInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, manager_id):
        try:
            
            manager = Manager.objects.get(id=manager_id)
        except Manager.DoesNotExist:
            return Response({"error": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = ManagerSerializer(manager)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EmployeeInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        try:
            
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = EmployeeSerializer(employee)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ValidateToken(APIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [AllowAny]  

    def post(self, request):
        token = request.headers.get('Authorization')  
        if not token:
            return Response({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        token_key = token.split("Token ")[-1]  
        try:
            token_obj = Token.objects.get(key=token_key)  
            return Response({"message": "Token is valid", "user_id": token_obj.user.id}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)