from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import UserActivity,UserMessage,UserActivity,UserAccount
from accounts.serializers import UserMessageSerializer,UserActivitySerializer
from .models import Activity, Class
from .serializers import ActivitySerializer, ActivitySearchSerializer, ClassSerializer
from .models import PersonalChatMessage
from .serializers import PersonalChatMessageSerializer
from accounts.models import UserAccount, UserInfo, UserImage
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.shortcuts import get_object_or_404

from accounts.enums import Message_e,Activity_e,M_State_e
from accounts.views import reject_message
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.core.paginator import Paginator
from accounts.models import UserAccount
from accounts.required import delete_some
from accounts.serializers import UserImageSerializer

from django.db.models import Q
from django.db.models import Max
from dateutil import parser


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # print(data)

        Name = data.get('Name')
        CreatorID = data.get('CreatorID')
        ClassID1 = data.get('Class_search_for_ID1')
        ClassID2 = data.get('Class_search_for_ID2')
        CampusID = data.get('Campus_search_for_ID')
        Location = data.get('Location')
        Description = data.get('Description')

        StartDateOriginal = data.get('StartDate')
        # 提取前半部分和后半部分
        StartDatePart = StartDateOriginal.split()[0:4]  # 提取 "Wed Nov 27 2024"
        StartTimePart = StartDateOriginal.split()[10:11]  # 提取 "00:00:00"
        # 组合日期和时间
        StartCombinedDateTime = " ".join(StartDatePart) + " " + " ".join(StartTimePart)
        StartDate = datetime.strptime(StartCombinedDateTime, '%a %b %d %Y %H:%M:%S')

        DueDateOriginal = data.get('DueDate')
        # 提取前半部分和后半部分
        DueDatePart = DueDateOriginal.split()[0:4]  # 提取 "Wed Nov 27 2024"
        DueTimePart = DueDateOriginal.split()[10:11]  # 提取 "00:00:00"
        # 组合日期和时间
        DueCombinedDateTime = " ".join(DueDatePart) + " " + " ".join(DueTimePart)
        DueDate = datetime.strptime(DueCombinedDateTime, '%a %b %d %Y %H:%M:%S')

        # 检查 DueDate 是否小于等于 StartDate
        if DueDate > StartDate:
            return Response(
                {"message": "报名截止时间需早于活动开始时间", "errors": {"报名截止时间需早于活动开始时间"}},
                status=status.HTTP_405_METHOD_NOT_ALLOWED 
            )

        NeedRealName = data.get('NeedRealName')
        # NumCurrent = data.get('NumCurrent')
        NumLimit = data.get('NumLimit')

        

        try:
            if(ClassID2 is None):
                class_record = Class.objects.get(First=ClassID1)
                ClassID = class_record.ID
            else:
                class_record = Class.objects.get(First=ClassID1, Second=ClassID2)
                ClassID = class_record.ID
                
        except Class.DoesNotExist:
            return Response(
                {"message": "Class record not found", "errors": {"ClassID": "Class record not found"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = {
            'Name': Name,
            'CreatorID': CreatorID,
            'ClassID': ClassID,
            'CampusID': CampusID,
            'Location': Location,
            'Description': Description,
            'StartDate': StartDate,
            'DueDate': DueDate,
            'NeedRealName': NeedRealName,
            'NumLimit': NumLimit
        }
        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            now=serializer.save()
            headers = self.get_success_headers(serializer.data)
            temp1=UserActivity.objects.get(A_User_id=CreatorID)
            temp1.A_CreateActivity=temp1.A_CreateActivity+str(now.ActivityID)+','
            temp1.save()
            return Response(
                {"message": "Activity created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {"message": "Activity creation failed", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class ActivitySearchSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySearchSerializer

    def list(self, request, *args, **kwargs):
        index = int(request.query_params.get('index'))
        index = index - 1
        page_size = int(request.query_params.get('pageSize', 10))

        activities = Activity.objects.select_related('ClassID').all()

        # 总活动数
        total_activities_num = activities.count()

        # 分页
        activities = activities[index * page_size:(index + 1) * page_size]

        # 处理数据
        processed_activities = []
        for activity in activities:
            processed_activity = {
                'Name': activity.Name,
                'Kinds' : [activity.ClassID.First,activity.ClassID.Second],
                'Num': f"{activity.NumCurrent}/{activity.NumLimit}",  # 拼接NumNow和NumLimit
                'ActivityID': str(activity.ActivityID),
                'DueDate': activity.DueDate.strftime('%Y-%m-%d %H:%M:%S'),     
            }
            processed_activities.append(processed_activity)

        print(total_activities_num)

        return Response({
            'data': processed_activities,
            'total': total_activities_num
        }, status=status.HTTP_200_OK)


class GetClassView(APIView):
    def get(self, request):
        try:
            # 获取所有的一级类目
            first_categories = Class.objects.values('First').distinct()

            # 构建返回的数据结构
            data = []
            for first_category in first_categories:
                first_name = first_category['First']
                second_categories = Class.objects.filter(First=first_name).values('Second', 'ID')

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
                'message': 'noserve'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetActBasicAllView(APIView):
    def get(self, request):
        try:
            # 获取所有活动
            activities = Activity.objects.all()

            # 构建返回的数据结构
            data = []
            for activity in activities:
                data.append({
                    'ActivityID': str(activity.ActivityID),
                    'Name': activity.Name,
                    'ClassID': str(activity.ClassID_id),
                    'DueDate': activity.DueDate.strftime('%Y-%m-%d'),
                    'NumCurrent': str(activity.NumCurrent),
                    'NumLimit': str(activity.NumLimit)
                })

            return Response({
                'success': True,
                'message': 'ok',
                'data': data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'No serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetActBasicByClassView(APIView):
    def get(self, request, classID):
        try:
            # 尝试将 classID 转换为整数
            classID = int(classID)
        except ValueError:
            return Response({
                'success': False,
                'message': 'No such ID',
                'data': ""
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取指定 classID 的活动
            activities = Activity.objects.filter(ClassID_id=classID)

            # 构建返回的数据结构
            data = []
            for activity in activities:
                data.append({
                    'ActivityID': str(activity.ActivityID),
                    'Name': activity.Name,
                    'ClassID': str(activity.ClassID_id),
                    'DueDate': activity.DueDate.strftime('%Y-%m-%d'),
                    'NumCurrent': str(activity.NumCurrent),
                    'NumLimit': str(activity.NumLimit)
                })

            if not data:
                return Response({
                    'success': False,
                    'message': 'No such ID',
                    'data': ""
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': True,
                'message': 'ok',
                'data': data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'No serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchActivityView(APIView):
    def get(self, request, word):
        try:
            # 获取分页参数
            index = int(request.query_params.get('page', 0)) - 1
            page_size = int(request.query_params.get('pageSize', 10))

            # 完全匹配的活动
            exact_match_activities = Activity.objects.filter(Name__iexact=word).order_by('-CreateDate')

            # 部分匹配的活动
            partial_match_activities = Activity.objects.filter(Name__icontains=word).exclude(Name__iexact=word).order_by('-CreateDate')

            # 删除完全匹配的活动
            remaining_activities = Activity.objects.exclude(Name__iexact=word)

            # 部分字符匹配的活动
            partial_char_match_activities = Activity.objects.none()
            for char in word:
                partial_char_match_activities |= remaining_activities.filter(Name__icontains=char)

            # 去重
            partial_char_match_activities = partial_char_match_activities.distinct().order_by('-CreateDate')

            # 合并所有活动并去重
            all_activities = list(exact_match_activities) + list(partial_match_activities) + list(partial_char_match_activities)
            unique_activities = list(set(all_activities))

            # 总活动数
            total_activities_num = len(unique_activities)

            # 分页
            activities = unique_activities[index * page_size:(index + 1) * page_size]

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


class GetActivityDetailView(APIView):
    def get(self, request, activityID):
        try:
            # 尝试将 activityID 转换为整数
            activityID = int(activityID)
        except ValueError:
            return Response({
                'success': False,
                'message': 'not found',
                'data': ""
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取指定 activityID 的活动
            activity = Activity.objects.get(ActivityID=activityID)

            # 获取活动类目
            class_info = Class.objects.get(ID=activity.ClassID_id)

            # 获取活动的参与者 ID
            participants = activity.ParticipantsID.split(',') if activity.ParticipantsID else []

            # 构建返回的数据结构
            data = {
                'Name': activity.Name,
                'CampusID': activity.CampusID,
                'Location': activity.Location,
                'Class': {
                    'First': class_info.First,
                    'Second': class_info.Second
                },
                'StartDate': activity.StartDate.strftime('%Y-%m-%d %H:%M:%S'),
                'DueDate': activity.DueDate.strftime('%Y-%m-%d %H:%M:%S'),
                'NeedRealName': activity.NeedRealName,
                'NumLimit': str(activity.NumLimit),
                'NumCurrent': str(activity.NumCurrent),
                'Description': activity.Description,
                'Participants': participants,
                'CreatorID': activity.CreatorID
            }

            return Response({
                'success': True,
                'message': 'ok',
                'data': data
            }, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({
                'success': False,
                'message': 'not found',
                'data': ""
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetActivitiesByCategoryView(APIView):
    def get(self, request):
        index = int(request.query_params.get('page', 0)) - 1
        page_size = int(request.query_params.get('pageSize', 10))
        category = request.query_params.get('category', '全部')

        try:
            if category == '全部':
                # 返回全部活动中符合页数要求的活动
                activities = Activity.objects.select_related('ClassID').all()
            else:
                if ',' in category:
                    # 查询二级类目中的活动
                    first_category, second_category = category.split(',')
                    class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
                else:
                    # 查询一级类目中的活动
                    class_ids = Class.objects.filter(First=category).values_list('ID', flat=True)

                activities = Activity.objects.select_related('ClassID').filter(ClassID_id__in=class_ids)

            # 总活动数
            total_activities_num = activities.count()

            # 分页
            activities = activities[index * page_size:(index + 1) * page_size]

            # 处理数据
            processed_activities = []
            for activity in activities:
                PrintDueDate = str(activity.DueDate)
                PrintDueDate = PrintDueDate[:-6]
                processed_activity = {
                    'Name': activity.Name,
                    'Kinds': [activity.ClassID.First, activity.ClassID.Second],
                    'Num': f"{activity.NumCurrent}/{activity.NumLimit}",  # 拼接NumNow和NumLimit
                    'ActivityID': str(activity.ActivityID),
                    'DueDate': PrintDueDate,
                }
                processed_activities.append(processed_activity)

            return Response({
                'data': processed_activities,
                'total': total_activities_num
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# lists/views.py
# from accounts.models import UserAccount, UserInfo, UserImage
# from accounts.serializers import ParticipantSerializer

# class ParticipantViewSet(viewsets.ViewSet):
#     def retrieve(self, request, activityId=None):
#         activity = Activity.objects.get(ActivityID=activityId)
#         participant_ids = [int(pid) for pid in activity.ParticipantsID.strip(',').split(',')]
        
#         participants = []
#         # for participant_id in participant_ids:
#         #     user_account = UserAccount.objects.get(UserID=participant_id)
#         #     user_info = UserInfo.objects.get(I_User=user_account)
#         #     user_image = UserImage.objects.get(M_User=user_account)
            
#         #     participant_data = {
#         #         'id': user_account.UserID,
#         #         'name': user_info.Name,
#         #         'avatar': user_image.M_Image.url if user_image.M_Image else None
#         #     }
#         #     participants.append(participant_data)

#         print(participants)
#         return Response(participants)
     
class JoinActivityView(APIView):
    def post(self, request):
        user_id=request.data.get('u_id')
        activity_id=request.data.get('a_id')
        now_activity = Activity.objects.get(ActivityID=activity_id)
        if now_activity is None:
            return Response({
                'code': 0,
                'message': 'has no activity'
            }, status=status.HTTP_404_NOT_FOUND)
        creator_id=now_activity.CreatorID
        temp1=UserActivity.objects.get(A_User_id=user_id)
        temp1.A_WaiteActivity=temp1.A_WaiteActivity+str(activity_id)+','
        temp1.save()
        Serializer_UserMessageSerializer = UserMessageSerializer(data={'E_Op':Message_e.assort,'E_Content':str(activity_id)+','+str('request')+','+now_activity.Name,'E_State':M_State_e.Unread},context={'Recipient': creator_id,'Sender':user_id})
        if Serializer_UserMessageSerializer.is_valid():
            Serializer_UserMessageSerializer.save()
            return Response({
                'code': 0,
                'message': 'accept'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'code': 0,
                'message': 'something wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

class GetActivityStateView(APIView):
    def get(self, request):
        user_id = request.GET.get('u_id')
        activity_id = request.GET.get('a_id')
        temp = UserActivity.objects.get(A_User_id=user_id)
        joined_activity= temp.A_JoinActivity
        created_activity=temp.A_CreateActivity
        wait_activity=temp.A_WaiteActivity
        joined_list=set()
        created_list = set()
        wait_list = set()
        now=''
        for c in joined_activity:
            if c == ',':
                if now != '':
                    joined_list.add(now)
                    now=''
            else:
                now+=c
        for c in created_activity:
            if c == ',':
                if now != '':
                    created_list.add(now)
                    now=''
            else:
                now+=c
        for c in wait_activity:
            if c == ',':
                if now != '':
                    wait_list.add(now)
                    now=''
            else:
                now+=c
        if activity_id in joined_list:
            return Response({
                'message': 'Activity has been added'
            }, status=status.HTTP_200_OK)
        if activity_id in created_activity:
            return Response({
                'message': 'Activity was created by this user'
            }, status=status.HTTP_200_OK)
        if activity_id in wait_list:
            return Response({
                'message': 'Activity on hold'
            }, status=status.HTTP_200_OK)
        return Response({
                'message': 'Activity not acceded to'
            }, status=status.HTTP_200_OK)

class BreakeActivityView(APIView):
    def post(self, request):
        activity_id = request.data.get('a_id')
        activity_one = Activity.objects.get(ActivityID=activity_id)
        paritipants=activity_one.ParticipantsID
        if paritipants !=None:
            paritipants_list=paritipants.split(',')
            for paritipant in paritipants_list:
                if paritipant != '' :
                    user=UserAccount.objects.get(UserID=paritipant)
                    user_activity=user.Activity.first()
                    user_activity.A_JoinActivity=delete_some(user_activity.A_JoinActivity,activity_id)
                    user_activity.save()
                    accept_message = UserMessageSerializer(data={'E_Op': Message_e.assort, 'E_Content': activity_id + ',' + 'break'+','+activity_one.Name,'E_State': M_State_e.Unread},context={'Recipient': paritipant, 'Sender':activity_one.CreatorID})
                    if accept_message.is_valid():
                        accept_message.save()
                    else:
                        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        message_prepared = UserAccount.objects.get(UserID=activity_one.CreatorID).Message_Recipient.filter(E_Op=Message_e.assort, E_State=M_State_e.Unread)
        for done_message in message_prepared:
            if done_message.E_Content == activity_id + ',' + 'request'+','+activity_one.Name:
                reject_message(done_message)
        creator=UserAccount.objects.get(UserID=activity_one.CreatorID)
        creator_activity=creator.Activity.first()
        creator_activity.A_CreateActivity=delete_some(creator_activity.A_CreateActivity,activity_id)
        creator_activity.save()
        ChatMessage.objects.filter(RoomID= activity_one.RoomID).all().delete()
        activity_one.delete()
        return Response({'message':'accept'},status=status.HTTP_200_OK)


class GetChatMessagesView(APIView):
    def get(self, request):
        activity_id = request.query_params.get('ActivityId')
        page = int(request.query_params.get('page', 1))
        initial_timestamp = request.query_params.get('initialTimestamp')

        if not activity_id or not initial_timestamp:
            return Response({"error": "Activity ID and Initial Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not initial_timestamp:
            return Response({"error": "Initial Timestamp cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            initial_timestamp = parse_datetime(initial_timestamp)
        except ValueError:
            return Response({"error": "Invalid Initial Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询 RoomID 对应的聊天记录，时间戳小于等于 initial_timestamp，并按时间戳降序排列
        chat_messages = ChatMessage.objects.filter(
            RoomID=f'0{activity_id}',
            Timestamp__lte=initial_timestamp
        ).order_by('-Timestamp')

        # 分页，每页10条消息
        paginator = Paginator(chat_messages, 1000)

        if page > paginator.num_pages:
            return Response({
                "messages": [],
                "total_pages": paginator.num_pages,
                "current_page": page
            }, status=status.HTTP_200_OK)

        page_obj = paginator.get_page(page)

        # 将当前页的数据转换为列表，并按时间戳升序排列
        page_messages = list(page_obj.object_list)
        page_messages.sort(key=lambda x: x.Timestamp)

        # 序列化并返回数据
        serializer = ChatMessageSerializer(page_messages, many=True)

        return Response({
            "messages": serializer.data,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
        }, status=status.HTTP_200_OK)
    



# class SendMessageView(APIView):
#     def post(self, request):
#         activity_id = request.data.get('ActivityId')
#         user_id = request.data.get('UserID')
#         message = request.data.get('Message')
#         avatar_url = request.data.get('AvatarUrl')
#         timestamp = request.data.get('Timestamp')

#         if not activity_id or not user_id or not message or not avatar_url or not timestamp:
#             return Response({"error": "Activity ID, User ID, Message, AvatarUrl, and Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # 将前端发来的时间戳转换为 datetime 对象
#             timestamp = datetime.fromisoformat(timestamp)
#         except ValueError:
#             return Response({"error": "Invalid Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

#         # 将活动ID转换为聊天室ID
#         room_id = f'0{activity_id}'

#         # 创建聊天消息对象
#         chat_message = ChatMessage(RoomID=room_id, UserID=user_id, Message=message, AvatarUrl=avatar_url, Timestamp=timestamp)
#         chat_message.save()

#         return Response({"status": "success", "message": "Message sent successfully"}, status=status.HTTP_200_OK)
class SendMessageView(APIView):
    def post(self, request):
        activity_id = request.data.get('ActivityId')
        user_id = request.data.get('UserID')
        message = request.data.get('Message')
        avatar_url = request.data.get('AvatarUrl')
        timestamp = request.data.get('Timestamp')

        if not activity_id or not user_id or not message or not avatar_url or not timestamp:
            return Response({"error": "Activity ID, User ID, Message, AvatarUrl, and Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 使用 dateutil.parser 解析时间戳
            timestamp = parser.isoparse(timestamp)
        except ValueError:
            return Response({"error": "Invalid Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 将活动ID转换为聊天室ID
        room_id = f'0{activity_id}'

        # 创建聊天消息对象
        chat_message = ChatMessage(RoomID=room_id, UserID=user_id, Message=message, AvatarUrl=avatar_url, Timestamp=timestamp)
        chat_message.save()

        return Response({"status": "success", "message": "Message sent successfully"}, status=status.HTTP_200_OK)


class SearchAndFilterActivitiesView(APIView):
    def get(self, request):
        # 获取搜索关键词
        word = request.query_params.get('word', '')
        # 获取分页参数
        index = int(request.query_params.get('page', 0)) - 1
        page_size = int(request.query_params.get('pageSize', 10))
        # 获取类别参数
        category = request.query_params.get('category', '全部')

        try:
            if word:
                # 完全匹配的活动
                exact_match_activities = Activity.objects.filter(Name__iexact=word).order_by('-CreateDate')

                # 部分匹配的活动
                partial_match_activities = Activity.objects.filter(Name__icontains=word).exclude(Name__iexact=word).order_by('-CreateDate')

                # 删除完全匹配的活动
                remaining_activities = Activity.objects.exclude(Name__iexact=word)

                # 部分字符匹配的活动
                partial_char_match_activities = Activity.objects.none()
                for char in word:
                    partial_char_match_activities |= remaining_activities.filter(Name__icontains=char)

                # 去重
                partial_char_match_activities = partial_char_match_activities.distinct().order_by('-CreateDate')

                # 合并所有活动并去重
                all_activities = list(exact_match_activities) + list(partial_match_activities) + list(partial_char_match_activities)
                unique_activities = list(set(all_activities))

                # 将搜索结果转换为 QuerySet
                search_results = Activity.objects.filter(ActivityID__in=[activity.ActivityID for activity in unique_activities])
            else:
                # 如果没有搜索关键词，直接获取所有活动
                search_results = Activity.objects.all()

            if category != '全部':
                if ',' in category:
                    # 查询二级类目中的活动
                    first_category, second_category = category.split(',')
                    class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
                else:
                    # 查询一级类目中的活动
                    class_ids = Class.objects.filter(First=category).values_list('ID', flat=True)

                # 对搜索结果按类别筛选
                search_results = search_results.filter(ClassID_id__in=class_ids)

            # 总活动数
            total_activities_num = search_results.count()

            # 分页
            activities = search_results[index * page_size:(index + 1) * page_size]

            # 构建返回的数据结构
            data = []
            for activity in activities:
                class_info = Class.objects.get(ID=activity.ClassID_id)
                data.append({
                    'Name': activity.Name,
                    'Kinds': [class_info.First, class_info.Second],
                    'Num': f"{activity.NumCurrent}/{activity.NumLimit}",
                    'ActivityID': str(activity.ActivityID),
                    'DueDate': activity.DueDate.strftime('%Y-%m-%d %H:%M:%S'),
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

class SearchAndFilterDingYueActivitiesView(APIView):
    def get(self, request):
        # 获取搜索关键词
        word = request.query_params.get('word', '')
        # 获取分页参数
        index = int(request.query_params.get('page', 0)) - 1
        page_size = int(request.query_params.get('pageSize', 10))
        # 获取类别参数
        category = request.query_params.get('category', '全部')
        # 获取用户ID
        user_id = request.query_params.get('user_id')
        try:
            # 检查用户是否存在
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
            # 如果没有订阅任何类别，返回空结果
            if not subscribe_ids:
                return Response({
                    'success': True,
                    'message': 'ok',
                    'data': [],
                    'total': 0
                }, status=status.HTTP_200_OK)
            # 根据订阅的类别ID筛选活动
            search_results = Activity.objects.filter(ClassID_id__in=subscribe_ids)
            if word:
                # 完全匹配的活动
                exact_match_activities = search_results.filter(Name__iexact=word).order_by('-CreateDate')

                # 部分匹配的活动
                partial_match_activities = search_results.filter(Name__icontains=word).exclude(Name__iexact=word).order_by('-CreateDate')

                # 删除完全匹配的活动
                remaining_activities = search_results.exclude(Name__iexact=word)

                # 部分字符匹配的活动
                partial_char_match_activities = Activity.objects.none()
                for char in word:
                    partial_char_match_activities |= remaining_activities.filter(Name__icontains=char)

                # 去重
                partial_char_match_activities = partial_char_match_activities.distinct().order_by('-CreateDate')

                # 合并所有活动并去重
                all_activities = list(exact_match_activities) + list(partial_match_activities) + list(partial_char_match_activities)
                unique_activities = list(set(all_activities))

                # 将搜索结果转换为 QuerySet
                search_results = Activity.objects.filter(ActivityID__in=[activity.ActivityID for activity in unique_activities])
            else:
                # 如果没有搜索关键词，直接获取所有活动
                search_results = search_results.all()

            if category != '全部':
                if ',' in category:
                    # 查询二级类目中的活动
                    first_category, second_category = category.split(',')
                    class_ids = Class.objects.filter(First=first_category, Second=second_category).values_list('ID', flat=True)
                else:
                    # 查询一级类目中的活动
                    class_ids = Class.objects.filter(First=category).values_list('ID', flat=True)

                # 对搜索结果按类别筛选
                search_results = search_results.filter(ClassID_id__in=class_ids)

            # 总活动数
            total_activities_num = search_results.count()

            # 分页
            activities = search_results[index * page_size:(index + 1) * page_size]

            # 构建返回的数据结构
            data = []
            for activity in activities:
                class_info = Class.objects.get(ID=activity.ClassID_id)
                data.append({
                    'Name': activity.Name,
                    'Kinds': [class_info.First, class_info.Second],
                    'Num': f"{activity.NumCurrent}/{activity.NumLimit}",
                    'ActivityID': str(activity.ActivityID),
                    'DueDate': activity.DueDate.strftime('%Y-%m-%d %H:%M:%S'),
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

class GetActivityParticipantView(APIView):
    def get(self, request):
        activityId=request.GET.get('activityId')
        activity_now=Activity.objects.get(ActivityID=activityId)
        participant_list=activity_now.ParticipantsID.split(',')
        member=[]
        for participant in participant_list:
            if participant != '':
                temp={}
                user_now=UserAccount.objects.get(UserID=participant)
                temp['id']=participant
                temp['name']=user_now.Info.first().Name
                temp['avatar']='http://127.0.0.1:8000'+UserImageSerializer(user_now.Image.first()).data['M_Image']
                member.append(temp)
        return Response(member,status=status.HTTP_200_OK)

class GetLastMessagesView(APIView):
    def get(self, request):
        user_id = request.GET.get('u_id')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 查找与传入的用户ID聊过天的所有用户ID
            chat_partners = PersonalChatMessage.objects.filter(
                Q(SendUserID=user_id) | Q(ReceiveUserID=user_id)
            ).values('SendUserID', 'ReceiveUserID').annotate(
                latest_timestamp=Max('Timestamp')
            ).order_by('-latest_timestamp')

            # 去重并获取每个聊天伙伴的最后一条消息
            latest_messages = []
            seen_partners = set()
            for partner in chat_partners:
                partner_id = partner['SendUserID'] if partner['SendUserID'] != user_id else partner[
                    'ReceiveUserID']
                if partner_id in seen_partners:
                    continue
                seen_partners.add(partner_id)

                latest_message = PersonalChatMessage.objects.filter(
                    (Q(SendUserID=user_id) & Q(ReceiveUserID=partner_id)) |
                    (Q(SendUserID=partner_id) & Q(ReceiveUserID=user_id)),
                    Timestamp=partner['latest_timestamp']
                ).first()

                if latest_message:
                    latest_messages.append(latest_message)

            # 总消息数量
            total_messages_num = len(latest_messages)

            # 分页
            index = (page - 1) * page_size
            latest_messages = latest_messages[index:index + page_size]

            # 构建返回的数据结构
            data = []
            for message in latest_messages:
                partner_id = message.SendUserID if message.SendUserID != user_id else message.ReceiveUserID
                partner_info = UserInfo.objects.filter(I_User__UserID=partner_id).first()
                try:
                    partner_image = UserAccount.objects.get(UserID=partner_id).Image.first()
                except:
                    return Response({
                        'success': False,
                        'message': 'not found',
                        'data': ""
                    }, status=status.HTTP_400_BAD_REQUEST)
                partner_name = partner_info.Name if partner_info else "Unknown"
                data.append({
                    'user_image': 'http://127.0.0.1:8000' + UserImageSerializer(partner_image).data['M_Image'],
                    'user_id': partner_id,
                    'user_name': partner_name,
                    'message': message.Message,
                    'is_self': message.SendUserID == user_id,
                    'timestamp': message.Timestamp.strftime('%Y-%m-%d %H:%M:%S')
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
                'total': total_messages_num
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'no serve',
                'data': ""
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#管理员删除活动解散队伍
class DeleteTeamView(APIView):
    def delete(self, request):
        activity_id = request.data.get('ActivityID')
        if not activity_id:
            return Response({'error': 'ActivityID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取活动对象
        activity = get_object_or_404(Activity, ActivityID=activity_id)

        # 获取对应的 ChatMessage 对象
        chat_message = None
        if activity.RoomID:
            chat_message = get_object_or_404(ChatMessage, RoomID=activity.RoomID.RoomID)

        # 删除活动
        activity.delete()

        # 删除对应的 ChatMessage
        if chat_message:
            chat_message.delete()

        # 返回成功响应
        return Response({
            'success': True,
            'message': 'delete successful！'
        }, status=status.HTTP_200_OK)
    

class SendPersonalMessageView(APIView):
    def post(self, request):
        message = request.data.get('Message')
        send_user_id = request.data.get('SendUserID')
        receive_user_id = request.data.get('ReceiveUserID')
        timestamp = request.data.get('Timestamp')

        if not message or not send_user_id or not receive_user_id or not timestamp:
            return Response({"error": "Message, SendUserID, ReceiveUserID, and Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 将前端发来的时间戳转换为 datetime 对象
            timestamp = parser.isoparse(timestamp)
        except ValueError:
            return Response({"error": "Invalid Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建私聊消息对象
        personal_chat_message = PersonalChatMessage(
            SendUserID=send_user_id,
            ReceiveUserID=receive_user_id,
            Message=message,
            Timestamp=timestamp
        )
        personal_chat_message.save()

        return Response({"status": "success", "message": "Personal message sent successfully"}, status=status.HTTP_200_OK)


class GetPersonalChatMessagesView(APIView):
    def get(self, request):
        send_user_id = request.query_params.get('SendUserID')
        receive_user_id = request.query_params.get('ReceiveUserID')
        initial_timestamp = request.query_params.get('initialTimestamp')
        page = int(request.query_params.get('page', 1))

        if not send_user_id or not receive_user_id or not initial_timestamp:
            return Response({"error": "SendUserID, ReceiveUserID, and Initial Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not initial_timestamp:
            return Response({"error": "Initial Timestamp cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            initial_timestamp = parse_datetime(initial_timestamp)
        except ValueError:
            return Response({"error": "Invalid Initial Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询符合条件的私聊消息，时间戳小于等于 initial_timestamp，并按时间戳降序排列
        chat_messages = PersonalChatMessage.objects.filter(
            (Q(SendUserID=send_user_id) & Q(ReceiveUserID=receive_user_id)) |
            (Q(SendUserID=receive_user_id) & Q(ReceiveUserID=send_user_id)),
            Timestamp__lte=initial_timestamp
        ).order_by('-Timestamp')

        # 分页，每页10条消息
        paginator = Paginator(chat_messages, 10)

        if page > paginator.num_pages:
            return Response({
                "messages": [],
                "total_pages": paginator.num_pages,
                "current_page": page
            }, status=status.HTTP_200_OK)

        page_obj = paginator.get_page(page)

        # 将当前页的数据转换为列表，并按时间戳升序排列
        page_messages = list(page_obj.object_list)
        page_messages.sort(key=lambda x: x.Timestamp)

        # 构建返回的数据结构
        messages_data = []
        for message in page_messages:
            whether_current = message.SendUserID == send_user_id
            messages_data.append({
                "WhetherCurrent": whether_current,
                "Message": message.Message,
                "Timestamp": message.Timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            })

        return Response({
            "messages": messages_data,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
        }, status=status.HTTP_200_OK)


class GetLatestPersonalMessagesView(APIView):
    def get(self, request):
        send_user_id = request.query_params.get('SendUserID')
        receive_user_id = request.query_params.get('ReceiveUserID')
        current_timestamp = request.query_params.get('currentTimestamp')

        if not send_user_id or not receive_user_id or not current_timestamp:
            return Response({"error": "SendUserID, ReceiveUserID, and Current Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_timestamp = parse_datetime(current_timestamp)
        except ValueError:
            return Response({"error": "Invalid Current Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询符合条件的私聊消息，时间戳大于 current_timestamp，并按时间戳升序排列
        chat_messages = PersonalChatMessage.objects.filter(
            (Q(SendUserID=send_user_id) & Q(ReceiveUserID=receive_user_id)) |
            (Q(SendUserID=receive_user_id) & Q(ReceiveUserID=send_user_id)),
            Timestamp__gt=current_timestamp
        ).order_by('Timestamp')

        # 构建返回的数据结构
        messages_data = []
        for message in chat_messages:
            whether_current = message.SendUserID == send_user_id
            messages_data.append({
                "WhetherCurrent": whether_current,
                "Message": message.Message,
                "Timestamp": message.Timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            })

        return Response({
            "messages": messages_data
        }, status=status.HTTP_200_OK)

class GetChatMessagesView(APIView):
    def get(self, request):
        activity_id = request.query_params.get('ActivityId')
        page = int(request.query_params.get('page', 1))
        initial_timestamp = request.query_params.get('initialTimestamp')

        if not activity_id or not initial_timestamp:
            return Response({"error": "Activity ID and Initial Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not initial_timestamp:
            return Response({"error": "Initial Timestamp cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            initial_timestamp = parse_datetime(initial_timestamp)
        except ValueError:
            return Response({"error": "Invalid Initial Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询 RoomID 对应的聊天记录，时间戳小于等于 initial_timestamp，并按时间戳降序排列
        chat_messages = ChatMessage.objects.filter(
            RoomID=f'0{activity_id}',
            Timestamp__lte=initial_timestamp
        ).order_by('-Timestamp')

        # 分页，每页10条消息
        paginator = Paginator(chat_messages, 1000)

        if page > paginator.num_pages:
            return Response({
                "messages": [],
                "total_pages": paginator.num_pages,
                "current_page": page
            }, status=status.HTTP_200_OK)

        page_obj = paginator.get_page(page)

        # 将当前页的数据转换为列表，并按时间戳升序排列
        page_messages = list(page_obj.object_list)
        page_messages.sort(key=lambda x: x.Timestamp)

        # 序列化并返回数据
        serializer = ChatMessageSerializer(page_messages, many=True)

        return Response({
            "messages": serializer.data,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
        }, status=status.HTTP_200_OK)


class GetLatestMessagesView(APIView):
    def get(self, request):
        activity_id = request.query_params.get('ActivityId')
        current_timestamp = request.query_params.get('currentTimestamp')

        if not activity_id or not current_timestamp:
            return Response({"error": "Activity ID and Current Timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_timestamp = parse_datetime(current_timestamp)
        except ValueError:
            return Response({"error": "Invalid Current Timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询 activityId 对应的聊天记录，时间戳大于 current_timestamp
        chat_messages = ChatMessage.objects.filter(RoomID=f'0{activity_id}', Timestamp__gt=current_timestamp).order_by('Timestamp')

        # 序列化并返回数据
        serializer = ChatMessageSerializer(chat_messages, many=True)

        return Response({
            "messages": serializer.data
        }, status=status.HTTP_200_OK)


