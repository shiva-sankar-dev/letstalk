from django.shortcuts import render

# Create your views here.
def chatbot(request):
    return render(request,"chatbot.html")

def base(request):
    return render(request,"base.html")

def register(request):
    return render(request,"register.html")

def login(request):
    return render(request,"login.html")


