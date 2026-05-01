from django.shortcuts import render
from rest_framework import viewsets, permissions

from .serializers import DepartmentSerializer, EmployeeSerializer, LoginSerializer, UserDetailsSerializer, UserSerializer, SignupSerializer
from .models import Department, Employee, UserDetails, User
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate


# Create your views here.

# Implement views for the Employee model to perform CRUD operations (Create, Read, Update, Delete) using Django's generic views or function-based views. You can use Django's built-in forms or serializers to handle the data input and output for these operations. Additionally, you can implement authentication and permissions to restrict access to certain views based on user roles or permissions.
 
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all() #This line defines the queryset that will be used to retrieve the data for the viewset. In this case, it retrieves all instances of the Department model from the database.
    serializer_class = DepartmentSerializer #This line specifies the serializer class that will be used to convert the Department model instances into a format that can be easily rendered into JSON or other content types. The DepartmentSerializer class is responsible for defining how the data should be serialized and deserialized.
    permission_classes = [] # Means no permissions restrictions
    #permission_classes = [permissions.IsAuthenticated] # Means that only authenticated users can access the views provided by this viewset. If a user is not authenticated, they will receive a 401 Unauthorized response when trying to access the views. This is a common way to restrict access to certain views or actions in a Django REST Framework application, ensuring that only authorized users can perform certain operations on the data.

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all() 
    serializer_class = EmployeeSerializer 
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated]

# Include a searchfilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['Emp_name', 'Designation','Contact'] 
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated]     

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer 
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated]

# Registration API view
class SignupView(APIView):  # Subclass of Django view class -- Request passed will be REST framework's Request instances 
    permission_classes = [AllowAny]  # Allow anyone to access the signup view

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user_id': user.id,
                'username': user.username,
                'token': token.key,
                'role': user.groups.all()[0].id if user.groups.exists() else None
            }, status=status.HTTP_201_CREATED)
        else:
            res = { 'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
'''
Note:
1. Takes user input - username, password and group
2. Validates the input using SignupSerializer
3. Creates a new user if the input is valid
4. Creates a token for the user for authentication
5. Returns success response with user ID, username, token and role (group ID) if the user is created successfully
'''      


# APIView for handling login requests
class LoginAPIView(APIView):
    # This API will handle login and return token for authenticated user.
    permission_classes = [AllowAny]  # Allow anyone to access the login view,even if they are not authenticated
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                 '''We are retreving the token for the authenticated user.'''
                 token = Token.objects.get(user=user)
                 response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "username": user.username,
                    "role": user.groups.all()[0].id if user.groups.exists() else None,
                    "data": {
                        "token": token.key
                    }
                }
                 return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Bad Request",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
'''
Note:
1. This API allows users to login using their username and password. 
2. If credentials are valid,
    a. It returns a token(used for authentication in future API calls) also we will return the username and role(group ID)
3. If credentials are invalid, 
    a. It returns an error message with appropriate HHTTP status -> 401(Unauthorized) or 400(Bad Request) 
'''
