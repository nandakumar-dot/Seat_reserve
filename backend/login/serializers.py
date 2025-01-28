from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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