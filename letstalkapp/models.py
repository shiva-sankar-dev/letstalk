from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_image',default='profile_image/profile.png',null=True)
    
    def __str__(self):
        return self.user.username
    
class Chat(models.Model):
    userID = models.ForeignKey(Profile,on_delete=models.CASCADE)
    messages = models.TextField(null=True)
    checkuser = models.IntegerField(null=True)

    def __str__(self):
        return self.userID.user.username