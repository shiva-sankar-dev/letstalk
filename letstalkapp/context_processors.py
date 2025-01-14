from .models import *

def userprofile(request):
    user_id = ""
    if request.user.is_authenticated:
        user_id = Profile.objects.get(user=request.user.id)
        
    context ={
        "user_id":user_id,
    }
    return context