from django.db import models

class Class(models.Model):
    ID = models.AutoField(primary_key=True)
    First = models.CharField(max_length=255)
    Second = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return str(self.ID)

# class Activity(models.Model):
#     ActivityID = models.AutoField(primary_key=True)
#     Name = models.CharField(max_length=255)
#     CreatorID = models.CharField(max_length=255, null=True, blank=True)
#     ClassID = models.ForeignKey(Class, on_delete=models.CASCADE)  # 确保这是外键
#     CampusID = models.CharField(max_length=255)
#     Location = models.CharField(max_length=255, null=True, blank=True)
#     Description = models.CharField(max_length=255)
#     StartDate = models.DateTimeField(null=True, blank=True)
#     CreateDate = models.DateTimeField(auto_now_add=True)
#     DueDate = models.DateTimeField(null=True, blank=True)
#     NeedRealName = models.BooleanField(default=False, null=True, blank=True)
#     NumCurrent = models.IntegerField(default=1, null=True, blank=True)
#     NumLimit = models.IntegerField(null=True, blank=True)
#     RoomID = models.IntegerField(null=True, blank=True)
#     ParticipantsID = models.CharField(max_length=255, null=True, blank=True)
#
#     def __str__(self):
#         return self.Name
class Activity(models.Model):
    ActivityID = models.AutoField(primary_key=True)  # 保持活动ID为整数型
    Name = models.CharField(max_length=255)
    CreatorID = models.CharField(max_length=255, null=True, blank=True)
    ClassID = models.ForeignKey(Class, on_delete=models.CASCADE)
    CampusID = models.CharField(max_length=255)
    Location = models.CharField(max_length=255, null=True, blank=True)
    Description = models.CharField(max_length=255)
    StartDate = models.DateTimeField(null=True, blank=True)
    CreateDate = models.DateTimeField(auto_now_add=True)
    DueDate = models.DateTimeField(null=True, blank=True)
    NeedRealName = models.BooleanField(default=False, null=True, blank=True)
    NumCurrent = models.IntegerField(default=1, null=True, blank=True)
    NumLimit = models.IntegerField(null=True, blank=True)
    RoomID = models.ForeignKey('ChatMessage', on_delete=models.CASCADE, null=True, blank=True, related_name='activities')  # 修改为外键
    ParticipantsID = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # if not self.RoomID:
        #     # 自动分配聊天室ID
        #     self.RoomID = f'0{self.ActivityID}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name


class ChatMessage(models.Model):
    RoomID = models.CharField(max_length=255)  # 聊天室ID
    UserID = models.CharField(max_length=255)  # 修改为字符型
    Message = models.TextField()  # 消息内容
    AvatarUrl = models.CharField(max_length=255)  # 用户头像URL
    Timestamp = models.DateTimeField()  # 修改为不自动添加当前时间

    def __str__(self):
        return f"Message from {self.UserID} in Room {self.RoomID}"

    def __str__(self):
        return f"Message from {self.UserID} in Room {self.RoomID}"
    

# class Room(models.Model):
#     RoomID = models.IntegerField(primary_key=True, verbose_name="活动室ID")
#     TextID = models.CharField(max_length=255, verbose_name="文本ID")
#     UserIDs = models.JSONField(verbose_name="用户IDs")
#     Items = models.IntegerField(verbose_name="项目")
#     Total = models.IntegerField(verbose_name="总数")
#
#     def __str__(self):
#         return f"Room {self.RoomID}"
#     class Meta:
#         verbose_name = "活动室"
#         verbose_name_plural = "活动室"
#
#
# class ChatHistory(models.Model):
#     # 文本ID，整数类型，必填
#     TextID = models.IntegerField(primary_key=True, verbose_name="文本ID")
#     # 活动室ID，整数类型，必填
#     RoomID = models.IntegerField(verbose_name="活动室ID")
#     # 发送者ID，整数类型，必填
#     SenderID = models.IntegerField(verbose_name="发送者ID")
#     # 发送时间，字符串类型，必填
#     SendTime = models.CharField(max_length=255, verbose_name="发送时间")
#     # 内容，字符串类型，必填
#     Content = models.TextField(verbose_name="内容")
#     def __str__(self):
#         return f"ChatHistory {self.TextID}"
#     class Meta:
#         verbose_name = "聊天记录"
#         verbose_name_plural = "聊天记录"



class Application(models.Model):
    # 申请ID，整数类型，必填
    ApplyID = models.IntegerField(primary_key=True, verbose_name="申请ID")
    # 活动ID，整数类型，必填
    ActivityID = models.IntegerField(verbose_name="活动ID")
    # 申请人ID，整数类型，必填
    ApplicantID = models.IntegerField(verbose_name="申请人ID")
    # 状态，布尔类型
    Status = models.BooleanField(verbose_name="状态")
    # 时间，字符串类型，必填
    Time = models.CharField(max_length=255, verbose_name="时间")
    def __str__(self):
        return f"Application {self.ApplyID}"

    class Meta:
        verbose_name = "申请"
        verbose_name_plural = "申请"

class PersonalChatMessage(models.Model):
    SendUserID = models.CharField(max_length=255)
    ReceiveUserID = models.CharField(max_length=255)
    Message = models.TextField()
    Timestamp = models.DateTimeField()

    def __str__(self):
        return f"Message from {self.SendUserID} to {self.ReceiveUserID}"
    

