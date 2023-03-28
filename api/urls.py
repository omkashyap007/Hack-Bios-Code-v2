from django.urls import path
from api import views as api_views

urlpatterns = [
    path("change-device-state/" , api_views.changeDeviceState , name = "change-device-state") ,
    path("change-servo-device-state/" , api_views.changeServoDeviceState , name = "change-servo-device-state") ,
    path("login-user/" , api_views.userLoginPage , name = "api-user-login") , 
    
]
