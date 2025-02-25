
from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', chatbot,name="chatbot"),
    path('profile/', profile,name="profile"),
    path('base/', base,name="base"),
    path('answer/', answer,name="answer"),
    path('get_audio_data/', get_audio_data,name="get_audio_data"),
    path('', loginpage,name="loginpage"),
    path('register/', register,name="register"),
    path('logout_page/', logout_page,name="logout_page"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)