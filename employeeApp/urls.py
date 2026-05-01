from rest_framework.routers import DefaultRouter
from.import views
from django.urls import path

router = DefaultRouter() #DefaultRouter is a class provided by Django REST Framework that automatically generates URL patterns for viewsets. It simplifies the process of creating RESTful APIs by handling the routing of requests to the appropriate viewset methods based on the HTTP method and URL pattern.

# register urls for the viewsets
router.register(r'employees', views.EmployeeViewSet) #This line registers the EmployeeViewSet with the router, associating it with the URL pattern 'employees'. This means that any requests made to the 'employees' endpoint will be routed to the EmployeeViewSet for handling.
router.register(r'departments', views.DepartmentViewSet)
router.register(r'userdetails', views.UserDetailsViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls

# Each of these creates full CRUD urls for that model

'''
http://127.0.0.1:8000/admin/ -> admin panel

employees

CRUD -> Create, Read, Update, Delete

list of employees -> GET  
get one person -> GET (api/employees/1)
add employee -> POST (api/employees/)
edit employee -> PUT/PATCH (api/employees/1)
delete employee -> DELETE (api/employees/1)

'''


# Register User(SignupAPIview) is an APIView not a viewset
# To add an end point url of APIView - you should add directly to the urlpatterns using  Djanpath() function 
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='user-signup'),
    path('login/', views.LoginAPIView.as_view(), name='user-login'), 
]

# Include the router urls as well
urlpatterns += router.urls