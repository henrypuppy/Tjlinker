
from django.urls import path
from .views import RegisterView
from .views import UserInfoView
from .views import UserLoginView
from .views import EditInfoView
from .views import FindPasswordConfirmView
from .views import FindPasswordNewPassView
from .views import AdminLoginView
from .views import GetUserCreateActivityView
from .views import GetUserJoinActivityView
from .views import GetUserGroupMesssageView
from .views import GetUserSystemMesssageView
from .views import MesssageAcceptView
from .views import MesssageRejectView
from .views import SubscribeCategoryView
from .views import UnsubscribeCategoryView
from .views import SearchSubscribedActivitiesView
from .views import CheckSubscriptionStatusView
from .views import GetDingYueClassView  # 导入新的视图
from .views import LeaveActivity
from .views import DeleteActivityView
from .views import GetUserSystemMesssageView
from .views import MoveSomeoneView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/info/', UserInfoView.as_view(), name='users_info'),
    path('users/edit_info/', EditInfoView.as_view(), name='users_edit_info'),
    path('userlogin/', UserLoginView.as_view(), name='userlogin'),
    path('find_password_confirm/', FindPasswordConfirmView.as_view(), name='find_password_confirm'),
    path('find_password_newpass/', FindPasswordNewPassView.as_view(), name='find_password_newpass'),
    path('admin_login/', AdminLoginView.as_view(), name='admin_login'),
    path('get_user_create_activity/',GetUserCreateActivityView.as_view(),name='get_user_create_activity'),
    path('get_user_joined_activity/',GetUserJoinActivityView.as_view(),name='get_user_joined_activity'),
    path('get_user_group_message/',GetUserGroupMesssageView.as_view(),name='get_user_group_message'),
    path('get_user_system_message/',GetUserSystemMesssageView.as_view(),name='get_user_system_message'),
    path('accept_message/',MesssageAcceptView.as_view(),name='accept_message'),
    path('reject_message/',MesssageRejectView.as_view(),name='reject_message'),
    path('subscribe_category/', SubscribeCategoryView.as_view(), name='subscribe_category'),
    path('unsubscribe_category/', UnsubscribeCategoryView.as_view(), name='unsubscribe_category'),
    path('search_subscribed_activities/', SearchSubscribedActivitiesView.as_view(), name='search_subscribed_activities'),
    path('check_subscription_status/', CheckSubscriptionStatusView.as_view(), name='check_subscription_status'), 
    path('get_dingyue_class/', GetDingYueClassView.as_view(), name='get_dingyue_class'),
    path('get_dingyue_class/', GetDingYueClassView.as_view(), name='get_dingyue_class'),
    path('leave_activity/', LeaveActivity.as_view(), name='leave_activity'),
    path('delete_activity/', DeleteActivityView.as_view(), name='delete_activity'),
    path('delete_members/', MoveSomeoneView.as_view(), name='move_members'),
]
