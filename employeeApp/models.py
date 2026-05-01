from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Department(models.Model):
    Dept_id = models.AutoField(primary_key=True) 
    Dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Dept_name
    

class Employee(models.Model): #inheritance
    Emp_id = models.AutoField(primary_key=True) #AutoField is used to automatically generate a unique ID for each employee
    Emp_name = models.CharField(max_length=100) #CharField is used to store the employee's name 
    Salary = models.DecimalField(max_digits=10, decimal_places=2) #DecimalField is used to store the salary of the employee with a maximum of 10 digits and 2 decimal places
    Designation = models.CharField(max_length=100) 
    DateofJoining = models.DateField() #DateField is used to store the date of joining of the employee
    Contact = models.CharField(max_length=15) 
    Dept_id = models.ForeignKey(Department, on_delete=models.CASCADE) #ForeignKey is used to establish a relationship between the Employee and Department models, with a cascade delete behavior
    IsActive = models.BooleanField(default=True) #BooleanField is used to indicate whether the employee is active or not, with a default value of True

    def __str__(self):
        return self.Emp_name #This method is used to return the employee's name when the object is printed

 # on delete cascade: when a department is deleted, all employees associated with that department will also be deleted automatically.   
 # on delete set null: when a department is deleted, the Dept_id field of the associated employees will be set to null, allowing the employee records to remain in the database without an associated department.


# The UserDetails model is used to store additional information about the user, such as their profile details. It has a one-to-one relationship with the built-in User model, meaning that each user can have only one set of user details. The related_name attribute allows you to access the user details from the User model using the user_details attribute.
class UserDetails(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'user_details') 
    Phone_number = models.CharField(max_length=15)
    Email = models.EmailField()
    Address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username #Get the username from the built-in User class and return it as a string representation of the UserDetails object.

# User -> The User model is a built-in Django model that provides authentication and user management functionality. It includes fields such as username, password, email, and more. By using a one-to-one relationship with the User model, we can extend its functionality and store additional information about the user in the UserDetails model. 

# To generate token whenever a new user is created(using signals)
@receiver(post_save, sender=settings.AUTH_USER_MODEL) #This decorator is used to connect the create_auth_token function to the post_save signal of the User model. Whenever a new user is created and saved, the create_auth_token function will be called automatically.
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    
# post_save signal -> Do something after a model is save    