from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .gpio_functions import *
from django.contrib.auth import authenticate
# from .async_functions import *
import os
import json

BIOS_TOKEN = os.environ.get("BIOS_TOKEN").strip().lstrip().rstrip()

devices = {
    1 : [3 , 12 , "light" ,         gp.input(11) , "servo", 11] , 
    2 : [5 , 32 , "fan"   ,         gp.input(21) , "servo", 31] , 
    3 : [7 , 33 , "water_pump" ,    gp.input(7) , "servo", 35] ,
    4 : [8 , 38 , "fan" ,           gp.input(38) , "relay", None ] ,
    5 : [10, 40 , "fan" ,           gp.input(40) , "relay", None ] ,
}

@api_view(["POST"])
def changeDeviceState(request , *args ,**kwargs):
    response = {
        "data" : None , 
        "errors" : None , 
        "success" : False , 
        }
    postData = {}
    received_first_data = list(request.POST.keys())[0]
    print(f"fiirst dat : {received_first_data}")
    try :
        converted_data = json.loads(received_first_data)
        if type(converted_data) == type({}):
            postData = converted_data
    except :
        for key in request.POST:
            postData[key] = request.POST.get(key)
    print(f"This is post data : {postData}")
    button_number = int(postData.get("button_number"))
    state_change_value = int(postData.get("state_change_value"))
    print(button_number , state_change_value )
    try:
        Authorization = request.headers.get("Authorization")
    except :
        Authorization = None
    if not Authorization :
        response["errors"] = ["Please provide authentication details"]
        response["success"]  = False
        return Response(response)
    try :
        authorization_token = Authorization.split(" ")[1].strip().lstrip().rstrip()
    except :
        authorization_token = None
    if not authorization_token:
        response["errors"] = ["Token format Invalid !"]
        response["success"]  = False
        return Response(response)
    if authorization_token != BIOS_TOKEN :
        response["success"] = False
        response["errors"] = {
            "Authentication Error" : ["You are not allowed to access the api request !"]
            }
        response["success"]  = False
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
            response["success"]  = False
            return Response(response)
        authorization = headers["Authorization"]
        if not authorization : 
            response["errors"] = {
                "Authentication credentials required" : [
                    "Please provide authentication credentials !" ,
                ]
            }
            response["success"]  = False
            return Response(response)
        auth_token = authorization.split(" ")
        if len(auth_token) != 2 : 
            response["errors"] = {
                "Invalid form of Authentication credentials" : [
                    "Invalid authentication credentials !" ,
                ]
            }
            response["success"]  = False
            return Response(response)
        auth_token = auth_token[1]
        if BIOS_TOKEN != auth_token : 
            response["errors"] = {
                "Unauthorized user access" : [
                    "You are not allowed to access theh page !" ,
                ]
            }
            response["success"]  = False
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

@api_view(["GET"])
def checkDeviceStatus(request , *args , **kwargs):
    button_number = int(request.GET.get("button_number"))
    state = None
    for device in devices :
        if button_number == devices[device][1] :
            if devices[device][4] == "servo" :
                state = gp.input(devices[device][5])
            else :
                state = gp.input(devices[device][1])
    return Response(
        {
            "state" : int(state) ,
        }
    )