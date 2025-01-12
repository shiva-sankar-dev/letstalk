
from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', chatbot,name="chatbot"),
    path('base/', base,name="base"),
    path('', loginpage,name="loginpage"),
    path('register/', register,name="register"),
    path('logout_page/', logout_page,name="logout_page"),
]
