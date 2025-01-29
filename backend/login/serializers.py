from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Seat, TimeSlot, Reservation


class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        Manager.objects.create(user=user)
        return user

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    manager_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'manager_id']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        manager = Manager.objects.get(pk=validated_data['manager_id'])
        Employee.objects.create(user=user, manager=manager)
        return user

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
        if hasattr(user, 'manager_profile'):
            user_type = 'Manager'
        elif hasattr(user, 'employee_profile'):
            user_type = 'Employee'
        else:
            raise serializers.ValidationError("User does not have a valid profile.")

        
        token, created = Token.objects.get_or_create(user=user)

        return {
            'token': token.key,
            'user_id': user.id,
            'user_type': user_type
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
    seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Reservation
        fields = ['id', 'employee', 'seat', 'time_slot', 'reserved_at']

    def create(self, validated_data):
        employee = validated_data['employee']
        manager = employee.manager  
        
        if manager.balance < 10:
            raise serializers.ValidationError("Manager does not have enough balance for reservation.")

        manager.balance -= 10
        manager.save()

        validated_data['manager'] = manager

        return super().create(validated_data)

    
