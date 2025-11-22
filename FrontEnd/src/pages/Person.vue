<template>
  <div class="profile-page">
    <!-- Sidebar for User Info -->
    <aside class="user-info">
      <div class="avatar">
        <span class="avatar-icon">
          <img :src="user.avatarUrl" alt="User Avatar"
            style="width: 130px; height: 130px; margin-top: 7px; border-radius: 50%;" />
        </span>
        <span class="gender-icon">
          <!-- 如果 gender 为 1，显示男性图标 -->
          <img v-if="user.gender === '男'" src="@/assets/性别-男.svg" alt="Male Icon" />
          <!-- 否则显示女性图标 -->
          <img v-else src="@/assets/性别-女.svg" alt="Female Icon" />
        </span>
      </div>
      <h2 class="username">{{ user.username }}</h2>
      <p class="user-id">ID: {{ user.id }}</p>
      <p class="bio">个人简介: {{ user.bio }}</p>
      <div class="flex-container">
        <p class="tags">兴趣标签：</p>
        <div class="interest">
          <el-tag v-for="tag in user.tags" :key="tag" type="info">{{ tag }}</el-tag>
        </div>
      </div>
      <button class="edit-btn" @click="editUserInfo">编辑个人资料</button>
      <button class="home-btn" @click="router.push('/home')">回到主页</button>
      <button class="logout-btn" @click="router.push('/welcome')">退出登录</button>
    </aside>

    <!-- Main Content for Messages -->
    <main class="messages">
      <!-- 上方标签页 -->
      <el-tabs type="border-card">
        <el-tab-pane label="我的组队">
          <div class="content">
            <aside class="menu">
              <el-menu active-text-color="#8e72ff" background-color="#ffffff" class="el-menu-vertical-demo"
                default-active="1" text-color="#000" @open="handleOpen" @close="handleClose">
                <el-menu-item index="1" @click="showCreatedTeams">
                  <span>我发起的组队</span>
                </el-menu-item>
                <el-menu-item index="2" @click="showJoinedTeams">
                  <span>我加入的组队</span>
                </el-menu-item>
              </el-menu>
            </aside>

            <main v-if="activeContent === 'joinedTeams'" class="message-list">
              <div class="activity-card">
                <ActivityBasic v-for="(activity, index) in joinedActivities"
                  :key="activity.ActivityID"
                  :Name="activity.Name"
                  :Kinds="activity.Kinds"
                  :Num="activity.Num"
                  :DueDate="activity.DueDate"
                  :ActivityID="activity.ActivityID"
                  :top="`${index * 110 + 15}px`"
                  :left="'210px'"
                  />
              </div>
              <el-pagination
                layout="prev, pager, next"
                :total="total_joined"
                :page-size="pageSize"
                :current-page="currentPage_joined"
                @current-change="handlePageChange_joined"
                class="pagination"
              />
            </main>

            <main v-if="activeContent === 'createdTeams'" class="message-list">
              <div class="activity-card">
                <ActivityBasic v-for="(activity, index) in createdActivities"
                  :key="activity.ActivityID"
                  :Name="activity.Name"
                  :Kinds="activity.Kinds"
                  :Num="activity.Num"
                  :DueDate="activity.DueDate"
                  :ActivityID="activity.ActivityID"
                  :top="`${index * 110 + 15}px`"
                  :left="'210px'"
                  />
              </div>
              <el-pagination
                layout="prev, pager, next"
                :total="total_created"
                :page-size="pageSize"
                :current-page="currentPage_created"
                @current-change="handlePageChange_created"
                class="pagination"
              />
            </main>

          </div>

        </el-tab-pane>

        <el-tab-pane label="消息">
          <div class="content">
            <aside class="menu">
              <el-menu active-text-color="#8e72ff" background-color="#ffffff" class="el-menu-vertical-demo"
                default-active="1" text-color="#000" @open="handleOpen" @close="handleClose">
                <el-sub-menu index="1">
                  <template #title>
                    <span>我的消息</span>
                  </template>
                  <el-menu-item-group>
                    <el-menu-item index="1-1" @click="showGroupMessage">组队消息</el-menu-item>
                    <el-menu-item index="1-2" @click="showPrivateChat">私聊消息</el-menu-item>
                  </el-menu-item-group>
                </el-sub-menu>
                <el-menu-item index="2" @click="showSysMessage">
                  <span>系统消息</span>
                </el-menu-item>
              </el-menu>
            </aside>

            <main v-if="activeContent === 'GroupMessage'" class="message-list">
              <div style="height: 550px"><MessageItem
                v-for="message in groupMessages"
                :type="message.type"
                :title="message.activityName"
                :name="message.relevantPerson.name"
                :id="message.relevantPerson.id"
                :time="message.time"
                :m_id="message.m_id"
                :status="message.status"
                @refresh-data="fetchGroupMessages"
                @refresh-created-group="fetchCreatedActivities"
              />
              </div>
              <el-pagination
                layout="prev, pager, next"
                :total="total_group_message"
                :page-size="pageSize"
                :current-page="currentPage_group_message"
                @current-change="handlePageChange_group_message"
                class="pagination1"
              />
            </main>

            <main v-if="activeContent === 'SysMessage'" class="message-list">
              <div style="height: 550px"><MessageItem
                v-for="message in sysMessages"
                :type="message.type"
                :title="message.activityName"
                :time="message.time"
                :m_id="message.m_id"
                :status="message.status"
                @refresh-data="fetchSysMessages"
                @refresh-created-group="fetchCreatedActivities"
              />
              </div>
              <el-pagination
                layout="prev, pager, next"
                :total="total_sys_message"
                :page-size="pageSize"
                :current-page="currentPage_sys_message"
                @current-change="handlePageChange_sys_message"
                class="pagination1"
              />
            </main>

            <main v-if="activeContent === 'ChatMessage'" class="message-list">
              <div style="height: 550px"><ChatMessageItem
                v-for="message in chatMessages"
                :avatar="message.user_image"
                :time="message.timestamp"
                :name="message.user_name"
                :id="message.user_id"
                :content="message.message"
              />
              </div>
              <el-pagination
                layout="prev, pager, next"
                :total="total_chat_message"
                :page-size="pageSize"
                :current-page="currentPage_chat_message"
                @current-change="handlePageChange_chat_message"
                class="pagination1"
              />
            </main>

          </div>
        </el-tab-pane>
      </el-tabs>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ActivityBasic from "@/components/ActivityBasic.vue";
import MessageItem from '@/components/MessageItem.vue';
import ChatMessageItem from '@/components/ChatMessageItem.vue';

const router = useRouter()
const createdActivities = ref([]);
const joinedActivities = ref([]);
const groupMessages = ref([])
const sysMessages = ref([])
const chatMessages = ref([])

const total_created = ref(0)
const total_joined = ref(0)
const total_group_message = ref(0)
const total_sys_message = ref(0)
const total_chat_message = ref(0)

const currentPage_created = ref(1)
const currentPage_joined = ref(1)
const currentPage_group_message = ref(1)
const currentPage_sys_message = ref(1)
const currentPage_chat_message = ref(1)

const pageSize = 5

const userId = localStorage.getItem('userId')

const activeContent = ref('createdTeams'); // 当前激活的内容标识

const fetchJoinedActivities = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/get_user_joined_activity/`, {
      params: {
        index: currentPage_created.value,
        page_size: pageSize,
        u_id: userId, // 添加 created_by 参数
      },
    });
    joinedActivities.value = response.data.data;
    total_joined.value = response.data.num;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

const fetchCreatedActivities = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/get_user_create_activity/`, {
      params: {
        index: currentPage_created.value,
        page_size: pageSize,
        u_id: userId, // 添加 created_by 参数
      },
    });
    createdActivities.value = response.data.data;
    total_created.value = response.data.num;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

const fetchGroupMessages = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/get_user_group_message/`, {
      params: {
        index: currentPage_group_message.value,
        page_size: pageSize,
        u_id: userId, // 添加 created_by 参数
      },
    });
    groupMessages.value = response.data.data;
    total_group_message.value = response.data.num;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

const fetchSysMessages = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/get_user_system_message/`, {
      params: {
        index: currentPage_sys_message.value,
        page_size: pageSize,
        u_id: userId, // 添加 created_by 参数
      },
    });
    sysMessages.value = response.data.data;
    total_sys_message.value = response.data.num;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

const fetchChatMessages = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/get_last_messages/`, {
      params: {
        index: currentPage_chat_message.value,
        page_size: pageSize,
        u_id: userId, // 添加 created_by 参数
      },
    });
    chatMessages.value = response.data.data;
    total_chat_message.value = response.data.total;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
}

const handlePageChange_created = (page) => {
  currentPage_created.value = page
  fetchCreatedActivities(page)
}

const handlePageChange_joined = (page) => {
  currentPage_joined.value = page
  fetchJoinedActivities(page)
}

const handlePageChange_group_message = (page) => {
  currentPage_group_message.value = page
  fetchGroupMessages(page)
}

const handlePageChange_sys_message = (page) => {
  currentPage_sys_message.value = page
  fetchSysMessages(page)
}

const handlePageChange_chat_message = (page) => {
  currentPage_chat_message.value = page
  fetchChatMessages(page)
}

const showJoinedTeams = () => {
  activeContent.value = 'joinedTeams'
  fetchJoinedActivities(currentPage_joined.value)
};
const showCreatedTeams = () => {
  activeContent.value = 'createdTeams'
  fetchCreatedActivities(currentPage_created.value)
};
const showGroupMessage = () => {
  activeContent.value = 'GroupMessage'
  fetchGroupMessages(currentPage_group_message.value)
};
const showPrivateChat = () => { 
  activeContent.value = 'ChatMessage'
  fetchChatMessages(currentPage_chat_message.value)
};
const showSysMessage = () => {
  activeContent.value = 'SysMessage'
  fetchSysMessages(currentPage_sys_message.value)
};

onMounted(() => {
  fetchCreatedActivities(currentPage_created.value)
  fetchJoinedActivities(currentPage_joined.value)
  fetchGroupMessages(currentPage_group_message.value)
  fetchSysMessages(currentPage_sys_message.value)
  fetchChatMessages(currentPage_chat_message.value)
})
</script>

<script>
export default {
  data() {
    return {
      // activeContent: 'createdTeams', // 当前激活的内容标识
      user: {
        username: '111',
        bio: '这个人好懒什么都没有写~',
        tags: ['1', '2', '3'],
        avatarUrl: '',
        id: "",
        gender: '男',
      },
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中

      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 如果需要，可以在这里添加认证信息，例如：
            // 'Authorization': 'Bearer your-token'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.user = {
          username: data.Name,
          bio: data.Info,
          tags: data.Tag,
          gender: data.Sex ? '男' : '女', // 根据性别设置图标
          avatarUrl: data.Avatar, // 获取头像的URL
          id: userId
        };
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },

    editUserInfo() {
      // 跳转到编辑用户信息的页面
      this.$router.push({
        path: '/edituserinfo',
      });
      localStorage.setItem('userAvatar', this.user.avatarUrl);
      localStorage.setItem('userId', this.user.id);
      localStorage.setItem('userName', this.user.username);
      localStorage.setItem('userBio', this.user.bio);
      localStorage.setItem('userTags', this.user.tags);
      localStorage.setItem('userGender', this.user.gender);
    },

    // showJoinedTeams() {
    //   this.activeContent = 'joinedTeams';
    // },

    // showCreatedTeams() {
    //   this.activeContent = 'createdTeams';
    // },

    // showGroupMessage() {
    //   this.activeContent = 'GroupMessage';
    // },

    // showPrivateChat() {
    //   this.activeContent = 'ChatMessage';
    // },

    // showSysMessage() {
    //   this.activeContent = 'SysMessage';
    // },
  }
};

</script>

<style scoped>
.profile-page {
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  background-color: #ffffffbc;
  display: flex;
  gap: 20px;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.user-info {
  margin-top: 90px;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #ddd;
  padding-right: 50px;
  gap: 15px;
}

.menu {
  width: 140px;
  height: 600px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border-right: 1px solid #ddd;
  padding-right: 50px;
}

.content {
  display: flex;
  flex-direction: row;
}

.avatar {
  position: relative;
  font-size: 50px;
  background: #ddd;
  border-radius: 50%;
  width: 150px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: 20px;
}

.gender-icon {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 30px;
  /* 调整性别图标的宽度 */
  height: 30px;
  /* 调整性别图标的高度 */
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
  border: 2px solid #ddd;
}

.a-icon {
  margin-top: 18px;
  width: 170px;
  /* 调整性别图标内部图标的宽度 */
  height: 170px;
  /* 调整性别图标内部图标的高度 */
}

.g-icon {
  width: 20px;
  /* 调整性别图标内部图标的宽度 */
  height: 20px;
  /* 调整性别图标内部图标的高度 */
}

.username {
  font-size: 1.8em;
  margin-top: 10px;
}

.user-id {
  color: gray;
}

.bio {
  font-size: 0.8em;
  text-align: left;
  margin: 10px 0;
}

.tags {
  display: flex;
  gap: 5px;
  font-size: 0.8em;
}

.edit-btn {
  padding: 5px 10px;
  margin-top: 30px;
  border: none;
  background-color: #ded1e2;
  color: rgb(94, 94, 94);
  cursor: pointer;
  border-radius: 5px;
  font-size: small;
}

.logout-btn {
  padding: 5px 10px;
  border: none;
  background-color: #745b7a;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  font-size: small;
}

.home-btn {
  padding: 5px 10px;
  border: none;
  background-color: #9f8ba4;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  font-size: small;
}

.messages {
  margin-top: 70px;
  flex: 1;
}

.message-list {
  margin-top: 20px;
  margin-left: 50px;
  width: 600px;
}

.message {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ddd;
  position: relative;
}

.message-text {
  font-size: 0.8em;
}

.m-icon {
  font-size: 24px;
  margin-right: 20px;
}

.flex-container {
  width: 100%;
  /* 使容器占据父容器的全部宽度 */
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  /* 不换行 */
  align-items: center;
  justify-content: center;
}

.el-tabs--border-card>>>.el-tabs__header .el-tabs__item.is-active {
  background-color: #140085;
  border-left-color: #00000000;
  border-right-color: #00000000;
  color: #bcacff;
  border-radius: 10px;
  font-size: 20px;
}

.el-tabs--border-card>>>.el-tabs__header .el-tabs__item:not(.is-disabled):hover {
  color: #bcacff;
}

.el-tabs--border-card {
  background: var(--el-bg-color-overlay);
  border-radius: 10px;
}

.el-tabs--border-card>>>.el-tabs__header {
  background-color: #0b004b;
  border-bottom: 1px solid #0b004b;
  margin: 0;
  border-radius: 10px;
}

.el-menu {
  border-right: 0px;
}

.pagination {
  height: 10px;
  padding: 16px;
  background-color:white;
  margin-top: 545px;
  margin-left: 225px;
  position:fixed;
}

.pagination1 {
  height: 10px;
  padding: 16px;
  background-color:white;
  margin-bottom: 20px;
  margin-left: 225px;
  position:fixed;
}
</style>
