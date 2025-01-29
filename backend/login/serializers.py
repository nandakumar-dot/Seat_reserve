from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Seat, TimeSlot, Reservation



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
        fields = ['id', 'seat_number', 'is_available']
        
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

class ReservationSerializer(serializers.ModelSerializer):
    seat_name = serializers.CharField(source='seat.seat_number', read_only=True)
    time_slot_display = serializers.SerializerMethodField()
    employee_name = serializers.CharField(source='employee.user.username', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'employee', 'employee_name', 'seat', 'seat_name', 'time_slot', 'time_slot_display', 'reserved_at']

    def get_time_slot_display(self, obj):
        return f"{obj.time_slot.start_time.strftime('%H:%M')} - {obj.time_slot.end_time.strftime('%H:%M')}"

    def create(self, validated_data):
        employee = validated_data['employee']
        manager = employee.manager  
        
        if manager.balance < 10:
            raise serializers.ValidationError("Manager does not have enough balance for reservation.")

        manager.balance -= 10
        manager.save()

        validated_data['manager'] = manager

        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reservation_id'] = representation.pop('id')
        representation['employee_id'] = representation.pop('employee')
        return representation
    
