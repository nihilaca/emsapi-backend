from datetime import date
import re

from rest_framework import serializers
from .models import Department, Employee, UserDetails 

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group


# Create functions for validation
# Validation for DOJ as current date
def date_of_joining_validation(dateofJoining):
    today = date.today()
    if dateofJoining != today:
        raise serializers.ValidationError("Date of Joining must be Today")
    return dateofJoining

 # Validation for Employee name --only contains characters,no special characters 
def name_validation(emp_name):
    if len(emp_name) < 3 or not re.match("^[A-Za-z ]+$", emp_name):
        raise serializers.ValidationError("Name must be at least 3 characters long and contain only letters and spaces.")
    return emp_name

# Contact number validation
def contact_number_validation(contact_number):
    if not re.match("^[6-9][0-9]{9}$", contact_number):
        raise serializers.ValidationError("Contact number must be a 10-digit number.")
    return contact_number

'''
^ - Start 
[6-9] - The first digit must be between 6 and 9
[0-9]{9} - Followed by exactly 9 digits (0-9),so total 10 digits
$ - End
-- If your contact is IntegerField , regex may fail because of leading zeros. In that case, you can use CharField for contact number and apply the regex validation on it.
'''

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: #Meta class is used to specify the model and fields that should be included in the serialization process.
        model = Department  
        fields = '__all__' #This means that all fields of the Department model will be included in the serialized output. 

# Modify EmployeeSerializer to include the nested department details
# Adding appropriate validation to EmployeeSerializer 
# Regular expression is used to validate the contact number format, ensuring it consists of 10 digits and may optionally start with a country code.eg. +1234567890 or 1234567890.
# Modifying EmployeeSerializer  -- adding DOJ and Name validation
class EmployeeSerializer(serializers.ModelSerializer):        
    department = DepartmentSerializer(source='Dept_id',read_only=True)  
    DateofJoining = serializers.DateField(validators=[date_of_joining_validation])
    Emp_name = serializers.CharField(max_length =100,
                                      validators=[name_validation])
    Contact = serializers.CharField(max_length=15, validators=[contact_number_validation])
    class Meta:
        model = Employee
        #fields = '__all__' 
        fields = (
            'Emp_id',
            'Emp_name',
            'Salary',
            'Designation',
            'DateofJoining',
            'Contact',
            'IsActive',
            'Dept_id',
            'department' # Include the nested department details
        )

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):               
    class Meta:
        model = User
        fields = ('id', 'username')


# Create a Serializer for Signup
class SignupSerializer(serializers.ModelSerializer):
    # Add group name field
    group_name = serializers.CharField(write_only=True,required=False)  

    # Override the create method for adding the group name
    # Also change the password into hash before saving it
    def create(self, validated_data):
        # Remove group_name from validated_data to avoid issues with User model as it knows only username and password 
        self.group_name = validated_data.pop('group_name', None)  
        
        # Hash the password 
        validated_data['password'] = make_password(validated_data.get('password')) 

        # Create the user
        user = super(SignupSerializer, self).create(validated_data)

        # Add the user to the group_name if provided
        if self.group_name:
            group, created = Group.objects.get_or_create(name=self.group_name)
            user.groups.add(group)
        return user
        
    class Meta:
        model = User
        fields = ['username', 'password', 'group_name']

'''

Note :
1. Get and remove the group_name from the input data
2. Encrypt the password using make_password for security
3. Create the user with the cleaned data
4. If a groupname was given:
    a. Get or create the group with the given name
    b. Add the user to that group 
5. Return the created user    

'''


'''# Create a Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'password']'''

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']