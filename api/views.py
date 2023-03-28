from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .gpio_functions import *
from django.contrib.auth import authenticate
# from .async_functions import *
import os

BIOS_TOKEN = os.environ.get("BIOS_TOKEN").strip().lstrip().rstrip()

@api_view(["POST"])
def changeDeviceState(request , *args ,**kwargs):
    response = {
        "data" : None , 
        "errors" : None , 
        "success" : False , 
    }
    button_number = int(request.POST.get("button_number"))
    state_change_value = int(request.POST.get("state_change_value"))
    print(button_number , state_change_value )
    try:
        Authorization = request.headers.get("Authorization")
    except :
        Authorization = None
    if not Authorization :
        response["errors"] = ["Please provide authentication details"]
        return Response(response)
    try :
        authorization_token = Authorization.split(" ")[1].strip().lstrip().rstrip()
    except :
        authorization_token = None
    if not authorization_token:
        response["errors"] = ["Token format Invalid !"]
        return Response(response)
    if authorization_token != BIOS_TOKEN :
        response["success"] = False
        response["errors"] = {
            "Authentication Error" : ["You are not allowed to access the api request !"]
            }
        return Response(response)
    print(f"The value of button number is : {button_number}")
    print(f"The value of state change value is : {state_change_value}")
    state_changed = changePinStatus(button_number , state_change_value)
    if state_changed : 
        response["success"] = True
        response["data"] = f"Changed : {button_number} : {state_change_value}"
        return Response(
            response , 
        )
    else : 
        return Response(
            response , 
        )
    
@api_view(["POST"])
def changeServoDeviceState(request, *args , **kwargs):
    response = {
        "data" : None , 
        "errors" : None , 
        "success" : False , 
    }
    button_number = int(request.POST.get("button_number"))
    state_change_value = int(request.POST.get("state_change_value"))
    print(button_number , state_change_value )
    try:
        Authorization = request.headers.get("Authorization")
    except :
        Authorization = None
    print(Authorization)
    if not Authorization :
        response["errors"] = ["Please provide authentication details"]
        return Response(response)
    try :
        authorization_token = Authorization.split(" ")[1].strip().lstrip().rstrip()
    except :
        authorization_token = None
    print(authorization_token)
    if not authorization_token:
        response["errors"] = ["Token format Invalid !"]
        return Response(response)
    print(authorization_token)
    if authorization_token != BIOS_TOKEN :
        print("The bios token is not equal to auth token")
        response["success"] = False
        response["errors"] = {
            "Authentication Error" : ["You are not allowed to access the api request !"]
            }
        return Response(response)
    print(f"The value of button number is : {button_number}")
    print(f"The value of state change value is : {state_change_value}")
    state_changed = changeServoPinStatus(button_number , state_change_value)
    if state_changed : 
        response["success"] = True
        response["data"] = f"Changed : {button_number} : {state_change_value}"
        return Response(
            response , 
        )
    else : 
        return Response(
            response , 
        )
     
    
@api_view(["POST"])
def userLoginPage(request , *args , **kwargs) : 
    response = {
        "data" : None ,
        "errors" : None , 
        "success" : False ,
    }
    if request.method == "POST" : 
        headers = request.headers
        if "Authorization" not in headers : 
            response["errors"] = {
                "Authentication credentials required" : [
                    "Please provide authentication credentials !" ,
                ]
            }
            return Response(response)
        authorization = headers["Authorization"]
        if not authorization : 
            response["errors"] = {
                "Authentication credentials required" : [
                    "Please provide authentication credentials !" ,
                ]
            }
            return Response(response)
        auth_token = authorization.split(" ")
        if len(auth_token) != 2 : 
            response["errors"] = {
                "Invalid form of Authentication credentials" : [
                    "Invalid authentication credentials !" ,
                ]
            }
            return Response(response)
        auth_token = auth_token[1]
        if BIOS_TOKEN != auth_token : 
            response["errors"] = {
                "Unauthorized user access" : [
                    "You are not allowed to access theh page !" ,
                ]
            }
            return Response(response)
        

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username ,  password = password)
        if not user :
            response["errors"] = {
                "Invalid user" : [
                    "User details are mismatching !" ,
                ]
            }
        response["success"] = True 
        response["data"] = "User authentication done!"
        return Response(response)
    else : 
        return Response(
            {
                "method_not_allowed" : "Other methods are not allowed !"
            }
        )
