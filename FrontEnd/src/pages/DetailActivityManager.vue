<template>
  <div>
    <!-- 调用导航栏组件 -->
    <TopNavBarWithoutSearchManager :AdminId="AdminId" />
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
          <div class="event-header">
            <h1 class="event-title">{{ event.title }}</h1>
            <div class="event-tags">
              <el-tag v-for="tag in event.tags" :key="tag" type="info" class="tag">{{ tag }}</el-tag>
            </div>
            <span class="people-count">人数 {{ event.currentParticipants }}/{{ event.maxParticipants }}</span>

            <!-- 管理员删除活动 -->
            <div class="dissolve-button-container">
              <el-button type="danger" size="small" @click="deleteActivity">删除活动</el-button>
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
import TopNavBarWithoutSearchManager from "@/components/TopNavBarWithoutSearchManager.vue";
import { ElTag, ElScrollbar } from "element-plus";

const AdminId = localStorage.getItem('AdminId');
// console.log(AdminId);

export default {
  components: {
    TopNavBarWithoutSearchManager,
    ElTag,
    ElScrollbar,
  },
  data() {
    return {
      AdminId: AdminId,
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
    };
  },
  created() {
    this.fetchEventDetails();
  },
  methods: {
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
            joinedMembers: data.Participants, // 参与者ID数组
            description: data.Description, // 活动描述
            creatorId: data.CreatorID, // 创建者ID
          };
        } else {
          console.error("Failed to fetch event details:", responseData.message);
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
      }
    },
    async deleteActivity() {
      const adminId = this.AdminId; // 当前用户 ID
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/delete_activity/`;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            d_id: adminId,
            a_id: eventId,
          }), // 将管理员 ID 传递到后端
        });

        const responseData = await response.json();
        if (responseData.message === 'accept') {
          alert("活动已成功删除！");
          // 跳转或更新页面状态
          this.$router.push('/manager');
        } else {
          alert(responseData.message || "删除活动失败！");
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
        alert("删除活动失败！");
      }
    },

  },
};
</script>

<style scoped>
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
  position: absolute;
  /* margin-right: 150px; */
}

.chatroom-text {
  margin-left: 20px;
  color: #646464;
  cursor: pointer;
  font-size: 14px;
}

.chatroom-text:hover {
  text-decoration: underline;
  /* 鼠标悬停时增加下划线 */
}

.action-buttons {
  display: flex;
  align-items: center;
}
</style>
