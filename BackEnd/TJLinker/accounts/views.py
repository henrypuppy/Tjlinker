# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
# from .models import UserAccount
# import json
# import logging
#
# logger = logging.getLogger(__name__)
#
# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS"])  # 允许 POST 和 OPTIONS 方法
# def register(request):
#     if request.method == "OPTIONS":
#         # 处理 OPTIONS 请求
#         response = JsonResponse({"success": True})
#         response["Access-Control-Allow-Origin"] = "*"
#         response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#         response["Access-Control-Allow-Headers"] = "Content-Type"
#         return response
#
#     try:
#         # 解析 JSON 数据
#         data = json.loads(request.body)
#         user_id = data.get('id')
#         password = data.get('password')
#         ok_password = data.get('okPassword')
#         answer = data.get('answer')
#
#         logger.info(f"Received registration data: {data}")
#
#         # 检查用户ID是否已存在
#         if UserAccount.objects.filter(UserID=user_id).exists():
#             return JsonResponse({"success": False, "message": "Duplicate user IDs"}, status=409)
#
#         # 检查密码长度和一致性
#         if len(password) < 6 or password != ok_password:
#             return JsonResponse({"success": False, "message": "The parameter is incorrect"}, status=400)
#
#         # 创建新用户
#         UserAccount.objects.create(UserID=user_id, Password=password, Answer=answer)
#         logger.info(f"User {user_id} registered successfully")
#         return JsonResponse({"success": True, "message": "register successful"}, status=201)
#
#     except Exception as e:
#         logger.error(f"Error registering user: {e}")
#         return JsonResponse({"success": False, "message": "Server error"}, status=500)

from rest_framework import serializers
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount,UserImage,UserActivity
from .models import UserAccount, UserInfo, AdminAccount
from .serializers import UserAccountSerializer
from .serializers import UserInfoSerializer
from .serializers import UserImageSerializer
from .serializers import UserActivitySerializer
from .enums import Message_e
from .serializers import UserMessageSerializer
from .models import UserMessage
from .enums  import M_State_e
from datetime import timedelta
from lists.models import Activity, Class
from .required  import delete_some
from lists.models import ChatMessage
import re

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')
        ok_password = data.get('okPassword')
        answer = data.get('answer')

        # 检查用户ID是否已存在
        if UserAccount.objects.filter(UserID=user_id).exists():
            return Response({"success": False, "message": "ID已存在"}, status=status.HTTP_409_CONFLICT)

        # 检查密码长度和一致性
        if len(password) < 6 or password != ok_password:
            return Response({"success": False, "message": "密码不符合要求"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建新用户
        user_data = {
            'UserID': user_id,
            'Password': password,
            'Answer': answer
        }
        serializer_UserAccountSerializer = UserAccountSerializer(data=user_data)
        if serializer_UserAccountSerializer.is_valid():
            serializer_UserAccountSerializer.save()
        else:
            return Response({"success": False, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer_UserInfoSerializer = UserInfoSerializer(data={'Name': user_id},context={'UserID': user_id})
        if serializer_UserInfoSerializer.is_valid():
            serializer_UserInfoSerializer.save()
        else:
            print(serializer_UserInfoSerializer.errors)
            return Response({"success": False, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer_UserImageSerializer = UserImageSerializer(data={},context={'UserID': user_id})
        if serializer_UserImageSerializer.is_valid():
            serializer_UserImageSerializer.save()
        else:
            print(serializer_UserImageSerializer.errors)
            return Response({"success": False, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer_UserActivitySerializer = UserActivitySerializer(data={}, context={'UserID': user_id})
        if serializer_UserActivitySerializer.is_valid():
            serializer_UserActivitySerializer.save()
            return Response({"success": True, "message": "register successful"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer_UserImageSerializer.errors)
            return Response({"success": False, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')

        # 检查用户ID是否存在
        try:
            user = UserAccount.objects.get(UserID=user_id)
        except UserAccount.DoesNotExist:
            return Response({"success": False, "message": "has no such ID"}, status=status.HTTP_409_CONFLICT)

        # 检查密码是否匹配
        if user.Password != password:
            return Response({"success": False, "message": "Password and ID do not match"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 登录成功
        return Response({"success": True, "message": "login succeed"}, status=status.HTTP_201_CREATED)

class FindPasswordConfirmView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        answer = data.get('answer')

        # 检查用户ID是否存在
        try:
            user = UserAccount.objects.get(UserID=user_id)
        except UserAccount.DoesNotExist:
            return Response({"success": False, "message": "has no such ID"}, status=status.HTTP_400_BAD_REQUEST)

        # 检查答案是否匹配
        if user.Answer != answer:
            return Response({"success": False, "message": "answers are wrong"}, status=status.HTTP_401_UNAUTHORIZED)

        # 验证成功
        return Response({"success": True, "message": "ID match answers"}, status=status.HTTP_200_OK)


class FindPasswordNewPassView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')
        ok_password = data.get('okPassword')

        # 检查用户ID是否存在
        try:
            user = UserAccount.objects.get(UserID=user_id)
        except UserAccount.DoesNotExist:
            return Response({"success": False, "message": "has no such ID"}, status=status.HTTP_401_UNAUTHORIZED)

        # 检查两次密码是否一致
        if password != ok_password:
            return Response({"success": False, "message": "Two passwords do not match"},
                            status=status.HTTP_402_PAYMENT_REQUIRED)

        # 检查密码格式：8-20位，只允许数字或英文字母
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return Response({"success": False, "message": "password not meet the requirements"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 更新密码
        user.Password = password
        user.save()

        # 更新成功
        return Response({"success": True, "message": "new password set"}, status=status.HTTP_200_OK)

class AdminLoginView(APIView):
    def post(self, request):
        data = request.data
        admin_id = data.get('id')
        password = data.get('password')

        # 检查管理员ID是否存在
        try:
            admin = AdminAccount.objects.get(AdminID=admin_id)
        except AdminAccount.DoesNotExist:
            return Response({"success": False, "message": "Admin ID does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # 检查密码是否匹配
        if admin.Password != password:
            return Response({"success": False, "message": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        # 登录成功
        return Response({"success": True, "message": "Admin login successful"}, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    def get(self, request):
        try:
            #print(request.GET.get('id'))
            usercount = UserAccount.objects.get(UserID=request.GET.get('id'))
        except UserAccount.DoesNotExist:
            return Response({ "code": 0,"message": "用户ID不存在"}, status=status.HTTP_404_NOT_FOUND)
        userinfo = usercount.Info.all().values('Name', 'Tag', 'Info','Sex').first()
        userinfo["code"]=0
        str1=userinfo['Tag']
        list1=['','','']
        count=0
        for c in str1:
            if c != ',':
                list1[count]+=c
            else:
                count+=1
        list1=[item for item in list1 if item]
        userinfo['Tag']=list1
        userimage = usercount.Image.all().first()
        userinfo['Avatar']='http://127.0.0.1:8000'+UserImageSerializer(userimage).data['M_Image']
        return Response(userinfo, status=status.HTTP_200_OK)

class EditInfoView(APIView):
    def post(self, request):
        id=request.POST.get('id')
        usercount = UserAccount.objects.get(UserID=id)
        if request.POST.get('name') is not None:
            usercount.Info.update(Name=request.POST.get('name'))
        if request.POST.get('sex') is not None:
            temp=request.POST.get('sex')
            if temp=='true':
                usercount.Info.update(Sex=1)
            else:
                usercount.Info.update(Sex=0)
        if request.POST.get('intro') is not None:
            usercount.Info.update(Info=request.POST.get('intro'))
        if request.POST.getlist('tags') is not None:
            temp=request.POST.getlist('tags')
            str=''
            count=0
            for index in range(len(temp)):
                str+=temp[index]
                if(index!=len(temp)-1):
                    count=count+1
                    str+=','
            while count<2:
                count+=1
                str+=','
            usercount.Info.update(Tag=str)
        if request.FILES.get('image') is not None:
            a=UserImage.objects.get(M_User_id=id)
            a.M_Image=request.FILES.get('image')
            a.save()
        return Response({"code": 0, "message": "accepted"}, status=status.HTTP_200_OK)

class GetUserCreateActivityView(APIView):
    def get(self, request):
        user_id=request.GET.get('u_id')
        index=int(request.GET.get('index'))
        page_size=int(request.GET.get('page_size'))
        createactivity=UserAccount.objects.get(UserID=user_id).Activity.first().A_CreateActivity
        temp=createactivity.split(',')
        createlist = [s for s in temp if s != ""]
        temp={'num':0,'data':[]}
        for i in range((index-1)*page_size,index*page_size):
            if i>=len(createlist):
                break
            activity=Activity.objects.get(ActivityID=createlist[i])
            PrintDueDate = str(activity.DueDate)
            PrintDueDate = PrintDueDate[:-6]
            temp['data'].append({
                'ActivityID': str(activity.ActivityID),
                'Name': activity.Name,
                'Kinds': [activity.ClassID.First,activity.ClassID.Second],
                'DueDate': PrintDueDate,
                'Num': f"{activity.NumCurrent}/{activity.NumLimit}",
            })
        temp['num']=len(createlist)
        return Response(temp, status=status.HTTP_200_OK)

class GetUserJoinActivityView(APIView):
    def get(self, request):
        user_id=request.GET.get('u_id')
        index=int(request.GET.get('index'))
        page_size=int(request.GET.get('page_size'))
        joinactivity=UserAccount.objects.get(UserID=user_id).Activity.first().A_JoinActivity
        temp = joinactivity.split(',')
        joinlist = [s for s in temp if s != ""]
        temp={'num':0,'data':[]}
        for i in range((index-1)*page_size,index*page_size):
            if i>=len(joinlist):
                break
            activity=Activity.objects.get(ActivityID=joinlist[i])
            PrintDueDate = str(activity.DueDate)
            PrintDueDate = PrintDueDate[:-6]
            temp['data'].append({
                'ActivityID': str(activity.ActivityID),
                'Name': activity.Name,
                'Kinds': [activity.ClassID.First,activity.ClassID.Second],
                'DueDate': PrintDueDate,
                'Num': f"{activity.NumCurrent}/{activity.NumLimit}",
            })
        temp['num']=len(joinlist)
        return Response(temp, status=status.HTTP_200_OK)

class GetUserGroupMesssageView(APIView):
    def get(self, request):
        user_id = request.GET.get('u_id')
        index = int(request.GET.get('index'))
        page_size = int(request.GET.get('page_size'))
        groupmessage = UserAccount.objects.get(UserID=user_id).Message_Recipient.filter(E_Op=Message_e.assort).all().order_by('-E_timestamp')
        l=(index-1)*page_size
        r=(index)*page_size
        return_data={'num':0,'data':[]}
        for now in range(l,r):
            if now>=len(groupmessage):
                break
            now_content = groupmessage[now].E_Content
            parts = now_content.split(',')
            temp={}
            # now_activity=Activity.objects.get(ActivityID=parts[0])
            temp['activityName']=parts[2]
            temp['m_id'] = groupmessage[now].E_ID
            temp['type']=parts[1]
            temp['relevantPerson']={'id':groupmessage[now].E_Sender_id,'name':UserAccount.objects.get(UserID=groupmessage[now].E_Sender_id).Info.first().Name}
            temp['status']=groupmessage[now].E_State
            Timestamp=groupmessage[now].E_timestamp
            #Timestamp+= timedelta(hours=8)
            PrintDueDate1 = str(Timestamp)
            PrintDueDate = PrintDueDate1[:-13]
            temp['time']=PrintDueDate
            return_data['data'].append(temp)
        return_data['num']=len(groupmessage)
        return Response(return_data, status=status.HTTP_200_OK)

# class GetUserPrivateMesssageView(APIView):
#     def get(self, request):
#         user_id = request.GET.get('u_id')
#         index = int(request.GET.get('index'))
#         page_size = int(request.GET.get('page_size'))
#         privatemessage = UserAccount.objects.get(UserID=user_id).Message_Recipient.filter(E_Op=Message_e.private).all().order_by('E_timestamp')
#         l=(index-1)*page_size
#         r=(index)*page_size
#         return_data={'num':0,'data':[]}
#         for now in range(l,r):
#             if now>=len(privatemessage):
#                 break
#             now_content = privatemessage[now].E_Content
#             parts = now_content.split(',')
#             temp={}
#             now_activity=Activity.objects.get(ActivityID=parts[0])
#             temp['m_id'] = privatemessage[now].E_ID
#             temp['activityName']=now_activity.Name
#             temp['type']=parts[1]
#             temp['applicant']={'id':privatemessage[now].E_Sender_id,'name':UserAccount.objects.get(UserID=privatemessage[now].E_Sender_id).Info.first().Name}
#             temp['creator']={'id':now_activity.CreatorID,'name':UserAccount.objects.get(UserID=now_activity.CreatorID).Info.first().Name}
#             temp['status']=privatemessage[now].E_State
#             Timestamp=privatemessage[now].E_timestamp
#             PrintDueDate1 = str(Timestamp)
#             PrintDueDate = PrintDueDate1[:-13]
#             temp['time']=PrintDueDate
#             return_data['data'].append(temp)
#         return_data['num']=len(return_data['data'])
#         return Response(return_data, status=status.HTTP_200_OK)

class GetUserSystemMesssageView(APIView):
    def get(self, request):
        user_id = request.GET.get('u_id')
        index = int(request.GET.get('index'))
        page_size = int(request.GET.get('page_size'))
        systemmessage = UserAccount.objects.get(UserID=user_id).Message_Recipient.filter(E_Op=Message_e.system).all().order_by('E_timestamp')
        l=(index-1)*page_size
        r=(index)*page_size
        return_data={'num':0,'data':[]}
        for now in range(l,r):
            if now>=len(systemmessage):
                break
            now_content = systemmessage[now].E_Content
            parts = now_content.split(',')
            temp={}
            temp['activityName']=parts[2]
            temp['type']=parts[1]
            Timestamp=systemmessage[now].E_timestamp
            #Timestamp+= timedelta(hours=8)
            PrintDueDate1 = str(Timestamp)
            PrintDueDate = PrintDueDate1[:-13]
            temp['time']=PrintDueDate
            return_data['data'].append(temp)
        return_data['num']=len(systemmessage)
        return Response(return_data, status=status.HTTP_200_OK)

def reject_message(message):
    message.E_State = M_State_e.Reject
    message.save()
    content = message.E_Content
    parts = content.split(',')
    activity_one=Activity.objects.get(ActivityID=parts[0])
    reject_message = UserMessageSerializer(
        data={'E_Op': Message_e.assort, 'E_Content': parts[0] + ',' + 'reject'+','+activity_one.Name, 'E_State': M_State_e.Unread},
        context={'Recipient': message.E_Sender_id, 'Sender': message.E_Recipient_id})
    if reject_message.is_valid():
        reject_message.save()
    else:
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    reject_person = UserAccount.objects.get(UserID=message.E_Sender_id)
    reject_person_activity = reject_person.Activity.first()
    reject_person_activity.A_WaiteActivity=delete_some(reject_person_activity.A_WaiteActivity,parts[0])
    reject_person_activity.save()

class MesssageAcceptView(APIView):
    def post(self, request):
        m_id = request.data.get('m_id')
        message=UserMessage.objects.get(E_ID=m_id)
        message.E_State=M_State_e.Accept
        message.save()
        content=message.E_Content
        parts=content.split(',')
        activity_one = Activity.objects.get(ActivityID=parts[0])
        accept_message=UserMessageSerializer(data={'E_Op':Message_e.assort,'E_Content':parts[0]+','+'accept'+','+activity_one.Name,'E_State':M_State_e.Unread},context={'Recipient':message.E_Sender_id,'Sender':message.E_Recipient_id})
        if accept_message.is_valid():
            accept_message.save()
        else:
            return Response({'message':'error'},status=status.HTTP_400_BAD_REQUEST)
        accept_person=UserAccount.objects.get(UserID=message.E_Sender_id)
        accept_person_activity=accept_person.Activity.first()
        accept_person_activity.A_WaiteActivity=delete_some(accept_person_activity.A_WaiteActivity,parts[0])
        joined_activity=accept_person_activity.A_JoinActivity
        joined_activity+=parts[0]+','
        accept_person_activity.A_JoinActivity=joined_activity
        accept_person_activity.save()
        if activity_one.ParticipantsID != None:
            activity_one.ParticipantsID=activity_one.ParticipantsID+str(message.E_Sender_id)+','
        else:
            activity_one.ParticipantsID = str(message.E_Sender_id)+','
        activity_one.NumCurrent=activity_one.NumCurrent+1
        activity_one.save()
        if activity_one.NumCurrent>=activity_one.NumLimit:
            message_prepared=UserAccount.objects.get(UserID=message.E_Recipient_id).Message_Recipient.filter(E_Op=Message_e.assort,E_State=M_State_e.Unread)
            for done_message in message_prepared:
                if done_message.E_Content==parts[0]+','+'request':
                    reject_message(done_message)
        return Response({'message':'accept'},status=status.HTTP_200_OK)

class MesssageRejectView(APIView):
    def post(self, request):
        m_id = request.data.get('m_id')
        message=UserMessage.objects.get(E_ID=m_id)
        reject_message(message)
        return Response({'message':'accept'},status=status.HTTP_200_OK)
class LeaveActivity(APIView):
    def post(self, request):
        u_id = request.data.get('u_id')
        a_id = request.data.get('a_id')
        activity_one=Activity.objects.get(ActivityID=a_id)
        User= UserAccount.objects.get(UserID=u_id)
        if(activity_one.CreatorID==User.UserID):
            return Response({'message':"creator cant leave"},status=status.HTTP_400_BAD_REQUEST)
        activity_one.ParticipantsID=delete_some(activity_one.ParticipantsID,u_id)
        activity_one.NumCurrent=activity_one.NumCurrent-1
        activity_one.save()
        user_activity=User.Activity.first()
        user_activity.A_JoinActivity=delete_some(user_activity.A_JoinActivity,a_id)
        user_activity.save()
        quit_message = UserMessageSerializer(data={'E_Op': Message_e.assort, 'E_Content': a_id + ',' + 'quit' + ',' + activity_one.Name,'E_State': M_State_e.Unread},context={'Recipient': activity_one.CreatorID, 'Sender': u_id})
        if quit_message.is_valid():
            quit_message.save()
        else:
            return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'message': "accept"}, status=status.HTTP_200_OK)

class SubscribeCategoryView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        category = request.data.get('category')

        try:
            user = UserAccount.objects.get(UserID=user_id)
        except UserAccount.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在',
                'data': ""
            }, status=status.HTTP_400_BAD_REQUEST)

        if ',' in category:
            # 查询二级类目中的活动
            first_category, second_category = category.split(',')
            class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
        else:
            # 查询一级类目中的活动
            class_ids = Class.objects.filter(First=category).values_list('ID', flat=True)

        # 将新的订阅ID添加到用户的SubscribeIDs中
        subscribe_ids = user.SubscribeIDs.split(',') if user.SubscribeIDs else []
        subscribe_ids.extend(map(str, class_ids))
        subscribe_ids = list(set(subscribe_ids))  # 去重
        subscribe_ids.sort(key=int)  # 按正序排序
        user.SubscribeIDs = ','.join(subscribe_ids)
        user.save()

        return Response({
            'success': True,
            'message': '订阅成功',
            'data': {
                'user_id': user.UserID,
                'subscribe_ids': user.SubscribeIDs
            }
        }, status=status.HTTP_200_OK)


class UnsubscribeCategoryView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        category = request.data.get('category')

        try:
            user = UserAccount.objects.get(UserID=user_id)
        except UserAccount.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在',
                'data': ""
            }, status=status.HTTP_400_BAD_REQUEST)

        if ',' in category:
            # 查询二级类目中的活动
            first_category, second_category = category.split(',')
            class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
        else:
            # 查询一级类目中的活动
            class_ids = Class.objects.filter(First=category).values_list('ID', flat=True)

        # 将需要取消订阅的ID从用户的SubscribeIDs中删除
        subscribe_ids = user.SubscribeIDs.split(',') if user.SubscribeIDs else []
        subscribe_ids = [id for id in subscribe_ids if id not in map(str, class_ids)]
        subscribe_ids.sort(key=int)  # 按正序排序
        user.SubscribeIDs = ','.join(subscribe_ids)
        user.save()

        return Response({
            'success': True,
            'message': '取消订阅成功',
            'data': {
                'user_id': user.UserID,
                'subscribe_ids': user.SubscribeIDs
            }
        }, status=status.HTTP_200_OK)


class SearchSubscribedActivitiesView(APIView):
    def get(self, request):
        try:
            # 获取分页参数
            page = int(request.query_params.get('page', 1))  # 默认页码为1
            page_size = int(request.query_params.get('pageSize', 10))
            user_id = request.query_params.get('user_id')

            # 计算基于0的索引
            index = (page - 1) * page_size

            try:
                user = UserAccount.objects.get(UserID=user_id)
            except UserAccount.DoesNotExist:
                return Response({
                    'success': False,
                    'message': '用户不存在',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取用户订阅的类别ID
            subscribe_ids = user.SubscribeIDs.split(',') if user.SubscribeIDs else []

            # 查询订阅类别中的活动
            activities = Activity.objects.filter(ClassID_id__in=subscribe_ids).order_by('-CreateDate')

            # 总活动数
            total_activities_num = activities.count()

            # 分页
            activities = activities[index:index + page_size]

            # 构建返回的数据结构
            data = []
            for activity in activities:
                class_info = Class.objects.get(ID=activity.ClassID_id)
                data.append({
                    'Name': activity.Name,
                    'Kinds': [class_info.First, class_info.Second],
                    'Num': f"{activity.NumCurrent}/{activity.NumLimit}",
                    'ActivityID': str(activity.ActivityID),
                    'DueDate': activity.DueDate.strftime('%Y-%m-%d'),
                })

            if not data:
                return Response({
                    'success': False,
                    'message': 'not found',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': True,
                'message': 'ok',
                'data': data,
                'total': total_activities_num
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CheckSubscriptionStatusView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            category = request.data.get('category')

            if not user_id or not category:
                return Response({
                    'success': False,
                    'message': 'Missing user_id or category',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = UserAccount.objects.get(UserID=user_id)
            except UserAccount.DoesNotExist:
                return Response({
                    'success': False,
                    'message': '用户不存在',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取用户订阅的类别ID
            subscribe_ids = user.SubscribeIDs.split(',') if user.SubscribeIDs else []

            # 检查用户是否订阅了该类目
            if ',' in category:
                first_category, second_category = category.split(',')
                class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
            else:
                first_category = category
                # 获取该一级类目下的所有二级类目
                all_second_categories = Class.objects.filter(First=first_category).values_list('ID', flat=True)
                all_second_categories = set(map(str, all_second_categories))

                # 检查用户是否订阅了该一级类目下的所有二级类目
                is_subscribed = all_second_categories.issubset(set(subscribe_ids))

                return Response({
                    'success': True,
                    'message': 'ok',
                    'isSubscribed': is_subscribed
                }, status=status.HTTP_200_OK)

            is_subscribed = any(str(class_id) in subscribe_ids for class_id in class_ids)

            return Response({
                'success': True,
                'message': 'ok',
                'isSubscribed': is_subscribed
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDingYueClassView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')

            if not user_id:
                return Response({
                    'success': False,
                    'message': 'Missing user_id',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = UserAccount.objects.get(UserID=user_id)
            except UserAccount.DoesNotExist:
                return Response({
                    'success': False,
                    'message': '用户不存在',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取用户订阅的类别ID
            subscribe_ids = user.SubscribeIDs.split(',') if user.SubscribeIDs else []

            # 查询订阅类别中的类目
            subscribed_classes = Class.objects.filter(ID__in=subscribe_ids)

            # 构建返回的数据结构
            data = []
            first_categories = subscribed_classes.values('First').distinct()

            for first_category in first_categories:
                first_name = first_category['First']
                second_categories = subscribed_classes.filter(First=first_name).values('Second', 'ID')

                second_data = []
                for second_category in second_categories:
                    second_data.append({
                        'classname': second_category['Second'],
                        'classID': str(second_category['ID'])
                    })

                data.append({
                    'first': first_name,
                    'second': second_data
                })

            return Response({
                'success': True,
                'message': 'ok',
                'data': data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteActivityView(APIView):
    def post(self, request):
        activity_id = request.data.get('a_id')
        activity_one = Activity.objects.get(ActivityID=activity_id)
        paritipants = activity_one.ParticipantsID
        if paritipants != None:
            paritipants_list = paritipants.split(',')
            for paritipant in paritipants_list:
                if paritipant != '':
                    user = UserAccount.objects.get(UserID=paritipant)
                    user_activity = user.Activity.first()
                    user_activity.A_JoinActivity = delete_some(user_activity.A_JoinActivity, activity_id)
                    user_activity.save()
                    accept_message = UserMessageSerializer(data={'E_Op': Message_e.system,'E_Content': activity_id + ',' + 'delete' + ',' + activity_one.Name,'E_State': M_State_e.Unread},context={'Recipient': paritipant,'Sender': paritipant})
                    if accept_message.is_valid():
                        accept_message.save()
                    else:
                        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                    message_prepared = UserAccount.objects.get(UserID=paritipant).Message_Recipient.filter(E_Op=Message_e.assort)
                    for done_message in message_prepared:
                        done_message_content_list=done_message.E_Content.split(',')
                        if done_message_content_list[0] == activity_id:
                            print(done_message.E_ID)
                            done_message.delete()
        message_prepared = UserAccount.objects.get(UserID=activity_one.CreatorID).Message_Recipient.filter(E_Op=Message_e.assort)
        for done_message in message_prepared:
            done_message_content_list = done_message.E_Content.split(',')
            if done_message_content_list[0] == activity_id:
                if  done_message_content_list[1]=='request' and done_message.E_State=='Unread':
                    user_wait=done_message.E_Sender
                    user_wait_activity=user_wait.Activity.first()
                    user_wait_activity.A_WaiteActivity=delete_some(user_wait_activity.A_WaiteActivity,activity_id)
                    user_wait_activity.save()
                done_message.delete()
        message = UserMessageSerializer(data={'E_Op': Message_e.system, 'E_Content': activity_id + ',' + 'delete' + ',' + activity_one.Name,'E_State': M_State_e.Unread}, context={'Recipient':activity_one.CreatorID, 'Sender': activity_one.CreatorID})
        if message.is_valid():
            message.save()
        else:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        print(activity_one.CreatorID)
        creator = UserAccount.objects.get(UserID=activity_one.CreatorID)
        creator_activity = creator.Activity.first()
        s=creator_activity.A_CreateActivity
        creator_activity.A_CreateActivity  = delete_some(creator_activity.A_CreateActivity, activity_id)
        creator_activity.save()
        ChatMessage.objects.filter(RoomID=activity_one.RoomID).all().delete()
        activity_one.delete()
        return Response({'message': 'accept'}, status=status.HTTP_200_OK)

class MoveSomeoneView(APIView):
    def delete(self, request):
        id_list = request.data.get('id')
        a_id = request.GET.get('activityId')
        activity_one = Activity.objects.get(ActivityID=a_id)
        for u_id in id_list:
            User = UserAccount.objects.get(UserID=u_id)
            if (activity_one.CreatorID == User.UserID):
                return Response({'message': "creator cant leave"}, status=status.HTTP_400_BAD_REQUEST)
            activity_one.ParticipantsID = delete_some(activity_one.ParticipantsID, u_id)
            activity_one.NumCurrent = activity_one.NumCurrent - 1
            activity_one.save()
            user_activity = User.Activity.first()
            user_activity.A_JoinActivity = delete_some(user_activity.A_JoinActivity, a_id)
            user_activity.save()
            move_message = UserMessageSerializer(data={'E_Op': Message_e.assort, 'E_Content': a_id + ',' + 'move' + ',' + activity_one.Name,'E_State': M_State_e.Unread}, context={'Recipient': u_id, 'Sender': activity_one.CreatorID})
            if move_message.is_valid():
                move_message.save()
            else:
                return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "accept"}, status=status.HTTP_200_OK)

