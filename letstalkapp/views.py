from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from openai import OpenAI
from openai import OpenAIError
from dotenv import load_dotenv
import os
load_dotenv()
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings
from playsound import playsound
import base64

@login_required(login_url='loginpage')
def chatbot(request):
    user = request.user.id
    response_text = ""
    audio_data = ""

    if request.method == "GET":
        message = request.GET.get("message")

        if message:
            user_id = Profile.objects.get(user=user)
            Chat.objects.create(userID=user_id, messages=message,checkuser=0)
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant.",
                        },
                        {
                            "role": "user",
                            "content": message,
                        },
                    ],
                    model="gpt-4o",
                )
                
                

                response_text = chat_completion.choices[0].message.content
                print(response_text,"_________")
                user_id = Profile.objects.get(user=user)
                Chat.objects.create(userID=user_id, messages=response_text,checkuser=1)
                
                
                elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
                audio = elevenlabs_client.generate(
                   text=response_text,
                   voice="Alice"
                )
                print(audio)
                audio_bytes = b"".join(audio)
                audio_data = base64.b64encode(audio_bytes).decode('utf-8')
                if response_text:
                    return JsonResponse({"converted":True,"audio_data":audio_data,"replay":response_text})
            except Exception as e:
                response_text = "An error occurred while generating the response."
                print(f"Error: {e}")

    get_chat = Chat.objects.filter(userID__user=user)

    context = {
        "get_chat": get_chat,
        "response_text": response_text, 
        "audio_data": audio_data, 
    }
    return render(request, "chatbot.html", context)


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
