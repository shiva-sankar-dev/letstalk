from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='loginpage')
def chatbot(request):
    user = request.user.id
    if request.method == "GET":
        message = request.GET.get("message")
        if message :
            user_id = Profile.objects.get(user=user)
            Chat.objects.create(userID=user_id,messages=message)
    
    get_chat = Chat.objects.filter(userID__user=user)
    context = {
        "get_chat":get_chat,
    }        
    return render(request,"chatbot.html",context)

def base(request):
    return render(request,"base.html")

def loginpage(request):
    if request.method == "POST":
        username = request.POST["log_username"]
        log_password = request.POST["log_password"]
        user = authenticate(request, username=username,password = log_password)
        if user is not None:
            login(request,user) 
            return redirect("chatbot")
        else:
            messages.error(request,"Invalid email or password.")
            return redirect("loginpage")
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST["reg_username"]
        email = request.POST.get("reg_email")
        profile_picture = request.FILES.get("reg_profile_picture")
        password = request.POST.get("reg_password")
        if User.objects.filter(username = email).exists():
            return JsonResponse({"exists":True,"message":"Email already exist"})
        else:
            user_reg = User.objects.create_user(username=email,email=email)
            user_reg.set_password(password)
            user_reg.first_name = username
            user_reg.save()
            Profile.objects.create(user=user_reg,profile_picture=profile_picture)
            return JsonResponse({"added":True})
    
    return render(request,"login.html")

def logout_page(request):
    logout(request)
    return render(request,"login.html")
