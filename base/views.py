from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login 
from django.contrib.auth.decorators import login_required
import switches
switches = switches.devices


@login_required
def homePage(request , *args , **kwargs) :
    context = {"command" : 1}
    return render(request , "base/switchBoard.html" , context = context)

def loginPage(request , *args , **kwargs) : 
    if request.method == "POST" : 
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username ,  password = password)
        if not user :
            return render(request , "base/loginPage.html" , context = {"error" : "InValid Username and Password !"})
        if user : 
            login(request , user)
            return redirect("home-page")
    if request.method == "GET" : 
        return render(request, "base/loginPage.html" , context = {})
    return render(request , "base/homePage.html" , context = {})