
from django.urls import path
from .views import *

urlpatterns = [
    path('', chatbot,name="chatbot"),
    path('base/', base,name="base"),
    path('login/', login,name="login"),
    path('register/', register,name="register"),
]
