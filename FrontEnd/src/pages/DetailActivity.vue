<template>
  <div>
    <!-- 调用导航栏组件 -->
    <TopNavBarWithoutSearch :avatar="user.avatarUrl" :nickname="user.username" :userId="user.id" />
  </div>

  <!-- 活动详情页面内容 -->
  <div class="page-container">
    <!-- 蓝色长条 -->
    <div class="blue-bar">
      <span class="bar-text">活动详情</span>
    </div>
    <!-- 滑动区域 -->
    <div class="event-details-scroll">
      <el-scrollbar style="height: 680px;">
        <div class="event-details">
          <!-- 活动标题和标签 -->
          <!-- 活动标题和标签 -->
          <div class="event-header">
            <h1 class="event-title">{{ event.title }}</h1>
            <div class="event-tags">
              <el-tag v-for="tag in event.tags" :key="tag" type="info" class="tag">{{ tag }}</el-tag>
            </div>
            <span class="people-count">人数 {{ event.currentParticipants }}/{{ event.maxParticipants }}</span>

            <!-- 按钮 -->
            <div class="button">
              <div v-if="joinStatus === 'creator'" class="action-buttons">
                <div class="dissolve-button-container">
                  <el-button type="danger" size="small" @click="handleDissolveTeam">解散队伍</el-button>
                </div>
                <div class="chatroom-link">
                  <span @click="enterChatroom" class="chatroom-text">进入聊天室 ></span>
                </div>
              </div>

              <!-- 如果用户未加入且未提交申请 -->
              <div v-if="joinStatus === 'notjoined'" class="dissolve-button-container">
                <!-- 报名截止时间已过 -->
                <div v-if="isRegistrationClosed">
                  <el-button type="danger" size="small" disabled>活动报名截止</el-button>
                </div>
                <!-- 人数已满 -->
                <div v-else-if="isParticipantsFull">
                  <el-button type="danger" size="small" disabled>活动报名已满</el-button>
                </div>
                <!-- 正常加入按钮 -->
                <div v-else>
                  <el-button type="primary" size="small" @click="joinActivity">加入队伍</el-button>
                </div>
              </div>

              <!-- 如果用户已提交申请，显示待审核 -->
              <div v-if="joinStatus === 'waiting'" class="dissolve-button-container">
                <el-button type="primary" size="small" disabled>待审核</el-button>
              </div>

              <!-- 已经加入要退出 -->
              <div v-if="joinStatus === 'joined'" class="action-buttons">
                <div class="dissolve-button-container">
                  <el-button type="danger" size="small" @click="Quit">退出队伍</el-button>
                </div>
                <div class="chatroom-link">
                  <span @click="enterChatroom" class="chatroom-text">进入聊天室 ></span>
                </div>
              </div>

            </div>
          </div>

          <!-- 校区和地点 -->
          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>活动校区：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.campus }}</span>
              </div>
            </el-col>
            <el-col :span="2">
              <div class="info-item">
                <span>活动地点：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.location }}</span>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>活动时间：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.time }}</span>
              </div>
            </el-col>
            <el-col :span="2">
              <div class="info-item">
                <span>报名截止时间：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.registrationDeadline }}</span>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>是否实名：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.isRealName ? "是" : "否" }}</span>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>人数上限：</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span>{{ event.maxParticipants }}</span>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>活动详情：</span>
              </div>
            </el-col>
            <el-col :span="20">
              <div class="info-item">
                <p>{{ event.description }}</p>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>活动创建者：</span>
              </div>
            </el-col>
            <el-col :span="20">
              <div
                class="info-item"
                :class="{ 'disabled-click': isCreator }"
                @click="PrivateChat"
              >
                <span class="private-text">{{ creator.username }}</span>
                <p>（ID:{{ event.creatorId }}）</p>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-left: 70px; margin-bottom: 20px;">
            <el-col :span="2">
              <div class="info-item">
                <span>已加入人员：</span>
              </div>
            </el-col>
            <el-col :span="10">
              <div class="members-list-inline">
                <el-tag v-for="memberId in event.joinedMembers" :key="memberId" type="success" class="tag">
                  {{ memberId }}
                </el-tag>
              </div>
            </el-col>
          </el-row>

        </div>
      </el-scrollbar>
    </div>
  </div>
</template>

<script>
import TopNavBarWithoutSearch from "@/components/TopNavBarWithoutSearch.vue";
import router from "@/router";
import { ElTag, ElScrollbar } from "element-plus";

export default {
  components: {
    TopNavBarWithoutSearch,
    ElTag,
    ElScrollbar,
  },
  data() {
    return {
      creator: {
        username: '0',
        avatarUrl: '1', // 获取头像的URL
        id: '2',
      },
      user: {
        username: "111",
        avatarUrl: "",
        id: localStorage.getItem('userId'),
        isAdmin: localStorage.getItem('isAdmin'),
      },
      event: {
        title: "嘉定周末网球双打",
        campus: "嘉定校区",
        location: "嘉定校园网球场",
        category: {
          primary: "体育",
          secondary: "网球",
        },
        time: "2024年10月27日 17:00",
        registrationDeadline: "2024年10月25日 23:59",
        isRealName: true,
        maxParticipants: 4,
        currentParticipants: 3,
        tags: ["# 体育", "# 网球"],
        joinedMembers: [1, 2], // 用户ID数组
        description: "这是活动的详细内容",
        creatorId: "11111111",
      },
      joinStatus: 'notjoined',
      currentDate: new Date(), // 当前日期
    };
  },
  created() {
    this.fetchUserData();
    this.fetchEventDetails();
    this.fetchJoinStatus();
  },
  computed: {
    isRegistrationClosed() {
      // 比较当前时间是否超过报名截止时间
      return new Date(this.event.registrationDeadline) < this.currentDate;
    },
    isParticipantsFull() {
      // 检查当前参与人数是否已满
      return this.event.currentParticipants >= this.event.maxParticipants;
    },
    isCreator() {
      return this.user.id === this.event.creatorId;
    },
  },
  methods: {
    updateCurrentDate() {
      this.currentDate = new Date();
    },

    enterChatroom() {
      localStorage.setItem('activityName', this.event.title);
      localStorage.setItem('creatorId', this.event.creatorId);
      // activityId: localStorage.getItem('activityId')
      // userId: localStorage.getItem('userId')
      router.push('/chat');
    },

    PrivateChat() {
      if (this.user.id === this.event.creatorId) {
        console.log("当前用户是活动创建者，无法与自己聊天。");
        return;
      }
      localStorage.setItem('activityName', this.event.title);
      localStorage.setItem('another_person', this.event.creatorId);
      // activityId: localStorage.getItem('activityId')
      // userId: localStorage.getItem('userId')
      router.push('/chat-personal');
    },

    async fetchJoinStatus() {
      const userId = this.user.id;
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/get_activity_state/?u_id=${userId}&a_id=${eventId}`;
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        if (responseData.message === 'Activity has been added') {
          this.joinStatus = 'joined';
        }
        else if (responseData.message === 'Activity on hold') {
          this.joinStatus = 'waiting';
        }
        else if (responseData.message === 'Activity not acceded to') {
          this.joinStatus = 'notjoined';
        }
        else if (responseData.message === 'Activity was created by this user') {
          this.joinStatus = 'creator';
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
        alert("获取活动状态失败！");
      }
      this.updateCurrentDate(); // 刷新当前时间
    },

    async fetchUserData() {
      const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 如果需要，可以在这里添加认证信息，例如：
            //             'Authorization': 'Bearer your-token'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.user = {
          username: data.Name,
          avatarUrl: data.Avatar, // 获取头像的URL
          id: userId,
          isAdmin: localStorage.getItem('isAdmin')
        };
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },

    async fetchCreatorData() {
      const createorId = this.event.creatorId; // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${createorId}`; // 将userId放在URL查询字符串中
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 如果需要，可以在这里添加认证信息，例如：
            //             'Authorization': 'Bearer your-token'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.creator = {
          username: data.Name,
          avatarUrl: data.Avatar, // 获取头像的URL
          id: createorId
        };
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },

    async fetchEventDetails() {
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/get_activity_detail/${eventId}`;
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        if (responseData.success) {
          const data = responseData.data;
          // 映射到本地组件的 data 中
          this.event = {
            title: data.Name, // 活动名称
            campus: data.CampusID, // 校区
            location: data.Location, // 地点
            category: {
              primary: data.Class.First, // 一级分类
              secondary: data.Class.Second, // 二级分类
            },
            time: data.StartDate, // 活动开始时间
            registrationDeadline: data.DueDate, // 报名截止时间
            isRealName: data.NeedRealName, // 是否实名
            maxParticipants: parseInt(data.NumLimit), // 人数上限
            currentParticipants: parseInt(data.NumCurrent), // 当前参与人数
            tags: [data.Class.First, data.Class.Second], // 自动生成标签
            joinedMembers: data.Participants.filter((memberId) => memberId), // 参与者ID数组
            description: data.Description, // 活动描述
            creatorId: data.CreatorID, // 创建者ID
          };

          // 调用 fetchCreatorData 获取创建者数据
          await this.fetchCreatorData();
        } else {
          console.error("Failed to fetch event details:", responseData.message);
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
      }
    },

    async joinActivity() {
      const userId = this.user.id;
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/join_activity/`;
      const confirmation = confirm("确定要加入活动吗？");
      if (!confirmation) return;
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            u_id: userId,
            a_id: eventId,
          }), // 将用户ID传递到后端
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        await this.fetchJoinStatus();
        if (responseData.message === 'accept') {
          alert("请求已发送，等待活动创建者确认！");
        } else {
          alert(responseData.message || "加入活动失败！");
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
        alert("加入活动失败！");
      }
    },

    async handleDissolveTeam() {
      try {
        const confirmation = confirm("确定要解散队伍吗？");
        if (!confirmation) return;

        const eventId = localStorage.getItem('activityId'); // activityId
        const url = `http://127.0.0.1:8000/api/break_activity/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            a_id: eventId,
          }),
        });

        const responseData = await response.json();
        if (responseData.message === 'accept') {
          alert("队伍已解散！");
          // 跳转回活动列表页面或刷新当前页面
          this.$router.push("/home");
        } else {
          alert("解散失败：" + responseData.message);
        }
      } catch (error) {
        console.error("Error dissolving team:", error);
        alert("解散失败，请稍后重试。");
      }
    },

    async Quit() {
      try {
        const confirmation = confirm("确定要退出活动吗？");
        if (!confirmation) return;

        const eventId = localStorage.getItem('activityId'); // activityId
        const userId = localStorage.getItem('userId'); // activityId
        const url = `http://127.0.0.1:8000/api/leave_activity/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            a_id: eventId,
            u_id: userId,
          }),
        });

        const responseData = await response.json();
        if (responseData.message === 'accept') {
          alert("已退出！");
          // 跳转回活动列表页面或刷新当前页面
          this.$router.push("/home");
        } else {
          alert("退出失败：" + responseData.message);
        }
      } catch (error) {
        console.error("Error dissolving team:", error);
        alert("退出失败，请稍后重试。");
      }
    },

  },

  mounted() {
    // 定期更新当前时间，避免用户长时间停留页面后状态不一致
    setInterval(this.updateCurrentDate, 6000);
  },
};
</script>

<style scoped>
.disabled-click {
  pointer-events: none;
  color: gray;
  cursor: default;
}

.button {
  position: absolute;
  /* margin-right: 100px; */
}

.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.event-details-scroll {
  width: 100%;
  max-width: 1450px;
  margin-top: 10px;
}

.event-details {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
}

.event-title {
  font-size: 24px;
  font-weight: bold;
}

.event-header {
  width: 1200px;
  display: flex;
  align-items: center;
  /* 确保内容垂直居中 */
  justify-content: flex-start;
  /* 将内容分布到两端 */
  margin-left: 50px;
  margin-bottom: 25px;
  margin-top: 20px;
}

.event-tags {
  margin-left: 10px;
}

.people-count {
  margin-left: 10px;
}

.info-item {
  font-size: 14px;
  color: #555;
  display: flex;
  flex-direction: row;
}

.members-list-inline {
  display: flex;
  flex-wrap: wrap;
}

.tag {
  margin-right: 10px;
  /* margin-top: 5px; */
}

.blue-bar {
  display: flex;
  align-items: center;
  justify-content: start;
  background-color: #161676;
  color: #fff;
  width: 1450px;
  height: 60px;
  border-radius: 5px;
  margin-top: 110px;
}

.bar-text {
  font-size: 18px;
  font-weight: bold;
  margin-left: 20px;
}

.dissolve-button-container {
  margin-left: 1100px;
  /* margin-right: 150px; */
}

.chatroom-text {
  margin-left: 20px;
  color: #646464;
  cursor: pointer;
  font-size: 14px;
}

.private-text {
  /* margin-left: 20px; */
  color: #646464;
  cursor: pointer;
  font-size: 14px;
}

.chatroom-text:hover {
  text-decoration: underline;
  /* 鼠标悬停时增加下划线 */
}

.private-text:hover {
  text-decoration: underline;
  /* 鼠标悬停时增加下划线 */
}

.action-buttons {
  display: flex;
  align-items: center;
}
</style>
