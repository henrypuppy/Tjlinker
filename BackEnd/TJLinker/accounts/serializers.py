from rest_framework import serializers
from .models import UserAccount
from .models import UserInfo
from .models import UserImage
from .models import UserActivity
from .models import UserMessage



from rest_framework import serializers
from .models import UserAccount, UserInfo, UserImage

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['UserID', 'Password', 'Answer', 'SubscribeIDs']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['Name', 'Sex', 'Tag', 'Info']

    def create(self, validated_data):
        userinfo = UserInfo.objects.create(I_User=UserAccount.objects.get(UserID=self.context['UserID']), **validated_data)
        return userinfo

class UserImageSerializer(serializers.ModelSerializer):
    M_Image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = UserImage
        fields = ['M_Image']

    def create(self, validated_data):
        userimage = UserImage.objects.create(M_User=UserAccount.objects.get(UserID=self.context['UserID']), **validated_data)
        return userimage

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['A_CreateActivity','A_JoinActivity','A_WaiteActivity']
    def create(self, validated_data):
        useractivity = UserActivity.objects.create(A_User=UserAccount.objects.get(UserID=self.context['UserID']), **validated_data)
        return useractivity

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['E_Op','E_Content','E_State']
    def create(self, validated_data):
        usermessage = UserMessage.objects.create(E_Recipient=UserAccount.objects.get(UserID=self.context['Recipient']),E_Sender=UserAccount.objects.get(UserID=self.context['Sender']), **validated_data)
        return usermessage
