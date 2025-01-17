from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,StreamingHttpResponse
from django.conf import settings
from openai import OpenAI
from openai import OpenAIError
from dotenv import load_dotenv
import os
import json
load_dotenv()
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings
from playsound import playsound
import base64
from markdown import markdown


@login_required(login_url='loginpage')
def chatbot(request):
    user = request.user.id

                
                


                
                
                # elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
                # audio = elevenlabs_client.generate(
                #    text=response_text,
                #    voice="Alice"
                # )
                # print(audio)
                # audio_bytes = b"".join(audio)
                # audio_data = base64.b64encode(audio_bytes).decode('utf-8')


    get_chat = Chat.objects.filter(userID__user=user)

    context = {
        "get_chat": get_chat,
    }
    return render(request, "chatbot.html", context)

def generate_response(question):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        model="gpt-4o",
        stream=True,
    )
    for chunk in chat_completion:
        if chunk.choices[0].delta.content is not None:
            yield(chunk.choices[0].delta.content)
    
@csrf_exempt                
def answer(request):
    user = request.user.id
    response_text = ""
    
    data = json.loads(request.body)
    message = data.get('message', '')
    
    if message:
        user_id = Profile.objects.get(user=user)
        Chat.objects.create(userID=user_id, messages=message,checkuser=0)
           
    for chunk in generate_response(message):
        response_text += chunk
        
    user_id = Profile.objects.get(user=user)
    print(response_text,"+++++++++")
    
    Chat.objects.create(userID=user_id, messages=response_text,checkuser=1)
    response = StreamingHttpResponse(generate_response(message),status = 200,content_type = "text/plain")

    return response

@csrf_exempt
def get_audio_data(request):
    data = json.loads(request.body)
    botMessage = data.get('botMessage', '')
    print(f"Received message: {botMessage}")
    
    elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = elevenlabs_client.generate(
       text=botMessage,
       voice="Alice"
    )
    print(audio)
    audio_bytes = b"".join(audio)
    audio_data = base64.b64encode(audio_bytes).decode('utf-8')
    
    return JsonResponse({"audio_data": audio_data})
    
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


login_required(login_url="loginpage")
def profile(request):
    if request.user.is_authenticated:   
        
        user_details = Profile.objects.get(user = request.user)
        if request.method == "POST":
            
            update_username = request.POST["update_username"]
            update_email = request.POST["update_email"]
            update_profile_picture = request.FILES.get("update_profile_picture")

            user_details.user.first_name = update_username
            user_details.user.email = update_email
            user_details.user.username = update_email
            user_details.user.save()
            if update_profile_picture:
                user_details.profile_picture = update_profile_picture
                user_details.save()
            
            
            return redirect("profile")
        context = {
            "user_details":user_details,
        }
        
    else:
        return redirect("loginpage")
            

    return render(request,"profile.html",context)
