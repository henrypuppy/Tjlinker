from rest_framework import serializers
from .models import Activity, Class
from .models import ChatMessage
from .models import PersonalChatMessage

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'



class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['First', 'Second']

class ActivitySearchSerializer(serializers.ModelSerializer):
    Class1 = serializers.CharField(source='ClassID.First')
    Class2 = serializers.CharField(source='ClassID.Second')
    Numnow = serializers.IntegerField(source='NumCurrent')

    class Meta:
        model = Activity
        fields = ['ActivityID', 'Name', 'Class1', 'Class2', 'Numnow', 'NumLimit', 'DueDate']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['RoomID', 'UserID', 'Message', 'AvatarUrl', 'Timestamp']

class PersonalChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalChatMessage
        fields = ['SendUserID', 'ReceiveUserID', 'Message', 'Timestamp']