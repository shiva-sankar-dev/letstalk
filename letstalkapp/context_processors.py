from .models import *

def userprofile(request):
    dp= ""
    if request.user.is_authenticated:
        user_profile  = Profile.objects.get(user=request.user)
        dp = user_profile .profile_picture
        
    context ={
        "dp": dp,
    }
    return context