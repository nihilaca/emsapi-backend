from django.contrib import admin

from .models import Department, Employee, UserDetails
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(UserDetails)
admin.site.register(Token)