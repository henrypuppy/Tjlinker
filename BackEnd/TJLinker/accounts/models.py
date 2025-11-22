from django.db import models
from django.utils import timezone

class UserAccount(models.Model):
    UserID = models.CharField(max_length=128,unique=True, primary_key=True)
    Password = models.CharField(max_length=128)
    Answer = models.CharField(max_length=255)
    SubscribeIDs = models.CharField(max_length=255, default='',null=True,blank=True)

    def __str__(self):
        return f"User {self.UserID}"


class AdminAccount(models.Model):
    AdminID = models.CharField(max_length=20, unique=True)
    Password = models.CharField(max_length=128)

    def __str__(self):
        return f"Admin {self.AdminID}"


class UserInfo(models.Model):
    I_User = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='Info')
    Name = models.CharField(max_length=50)
    Sex = models.BooleanField(default=0)
    Tag = models.CharField(max_length=80, default='@,@,@')
    Info = models.CharField(max_length=500, default='这个人很懒什么都没有写')

    def __str__(self):
        return f"User {self.Name}"


class UserImage(models.Model):
    M_User = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='Image')
    M_Image = models.ImageField(upload_to='user_images/', default='user_images/default.png')

    def __str__(self):
        return f"User {self.M_User.UserID}"

class UserActivity(models.Model):
    A_User = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='Activity')
    A_CreateActivity = models.CharField(max_length=1000,default='')
    A_JoinActivity = models.CharField(max_length=1000,default='')
    A_WaiteActivity = models.CharField(max_length=1000,default='')
    def __str__(self):
        return f"User {self.A_User.UserID}"

class UserMessage(models.Model):
    E_ID = models.AutoField(primary_key=True)
    E_Recipient = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='Message_Recipient')
    E_Sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='Message_Sender')
    E_Op   = models.IntegerField()
    E_Content   =   models.CharField(max_length=200)
    E_State = models.CharField(max_length=20)
    E_timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"User {self.E_ID}"
