from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ManagerRegistrationSerializer,
    EmployeeRegistrationSerializer,
    LoginSerializer
)
from .models import Manager, Employee


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
    def get(self, request):
        managers = Manager.objects.all()
        data = [{'user_id': manager.user.id, 'username': manager.user.username, 'email': manager.user.email, 'balance': manager.balance} for manager in managers]
        return Response(data, status=status.HTTP_200_OK)


class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        data = [{'user_id': employee.user.id, 'username': employee.user.username, 'email': employee.user.email, 'manager': employee.manager.user.username} for employee in employees]
        return Response(data, status=status.HTTP_200_OK)

class ManagerBalanceView(APIView):
    def get(self, request, manager_id):
        try:
            manager = Manager.objects.get(user_id=manager_id)
            return Response({'manager_id':manager.user_id ,'balance': manager.balance}, status=status.HTTP_200_OK)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        
