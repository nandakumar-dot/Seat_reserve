from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Seat, TimeSlot, Reservation, SeatAvailability



class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    manager_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'manager_id']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        Manager.objects.create(user=user)
        return user
    
    def get_manager_id(self, obj):
        return obj.manager_profile.id if hasattr(obj, 'manager_profile') else None

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    manager_id = serializers.IntegerField(write_only=True)
    employee_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'manager_id' ,'employee_id']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        manager = Manager.objects.get(pk=validated_data['manager_id'])
        Employee.objects.create(user=user, manager=manager)
        return user
    
    def get_employee_id(self, obj):
        return obj.employee_profile.id if hasattr(obj, 'employee_profile') else None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        
        user_type = None
        user_id = None
        additional_id = None

        if hasattr(user, 'manager_profile'):
            user_type = 'Manager'
            user_id = user.id
            additional_id = user.manager_profile.id  
        elif hasattr(user, 'employee_profile'):
            user_type = 'Employee'
            user_id = user.id
            additional_id = user.employee_profile.id  
        else:
            raise serializers.ValidationError("User does not have a valid profile.")
        
        token, created = Token.objects.get_or_create(user=user)

        return {
            'token': token.key,
            'user_id': user_id,
            'user_type': user_type,
            'additional_id': additional_id,  # Either manager_id or employee_id
            'username': user.username  
        }
        

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['seat_id'] = representation.pop('id')
        return representation

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['slot_id'] = representation.pop('id')
        return representation

from rest_framework import serializers
from .models import Reservation, Seat, TimeSlot, Employee, Manager

class ReservationSerializer(serializers.ModelSerializer):
    seat_name = serializers.CharField(source='seat.seat_number', read_only=True)
    employee_name = serializers.CharField(source='employee.user.username', read_only=True)
    time_slot_display = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'employee', 'employee_name', 'seat', 'seat_name', 'time_slot', 'time_slot_display', 'reserved_at']

    def get_time_slot_display(self, obj):
        return f"{obj.time_slot.start_time.strftime('%H:%M')} - {obj.time_slot.end_time.strftime('%H:%M')}"

    def create(self, validated_data):
        employee = validated_data['employee']
        manager = employee.manager  
        seat = validated_data['seat']
        time_slot = validated_data['time_slot']

        # Check if the seat is available for the given time slot
        if not Reservation.is_seat_available(seat, time_slot):
            raise serializers.ValidationError("Seat is not available for this time slot.")

        # Check if the manager has enough balance
        if manager.balance < 10:
            raise serializers.ValidationError("Manager does not have enough balance for reservation.")

        # Deduct balance from the manager
        manager.balance -= 10
        manager.save()

        # Proceed to create the reservation
        validated_data['manager'] = manager

        # Update SeatAvailability to mark seat as unavailable
        seat_availability, created = SeatAvailability.objects.get_or_create(seat=seat, time_slot=time_slot)
        seat_availability.is_available = False
        seat_availability.save()

        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reservation_id'] = representation.pop('id')
        representation['employee_id'] = representation.pop('employee')
        return representation

class SeatAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatAvailability
        fields = ['seat', 'is_available']
    
class ManagerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'user_name', 'balance', 'employee_count']
        
class EmployeeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')
    manager_name = serializers.CharField(source='manager.user.username', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user_name', 'manager_name']