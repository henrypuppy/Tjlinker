<template>
  
  <div class="page-container">
    <div>
    <!-- 调用导航栏组件 -->
    <TopNavBarWithoutSearchManager :AdminId="AdminId" />
  </div>
    <div class="activity-card">
      <ActivityBasic
        v-for="(activity, index) in activities"
        :key="activity.ActivityID"
        :Name="activity.Name"
        :Kinds="activity.Kinds"
        :Num="activity.Num"
        :DueDate="activity.DueDate"
        :ActivityID="activity.ActivityID"
        :top="
          index % 2 === 0
            ? `${index * 55 + 50}px`
            : `${(index - 1) * 55 + 50}px`
        "
        :left="index % 2 === 0 ? '100px' : '800px'"
        :right="index % 2 === 0 ? '800px' : '100px'"
      />
    </div>

    <el-pagination
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="currentPage"
      @current-change="handlePageChange"
      class="pagination"
    />
    <!-- <button @click="fetchActivities(currentPage.value)" class="fetch-button">获取数据</button> -->
    <button @click="logout" class="logout-button">退出登录</button>
  </div>
</template>

<script setup lang='ts'>
import { ref, onMounted } from "vue";
import axios from "axios";
import ActivityBasic from "@/components/ActivityBasic.vue";
import { useRouter } from "vue-router";
const router = useRouter();
const logout = () => {
  localStorage.clear();
  router.push("/welcome");
};
const activities = ref<any[]>([
  {
    ActivityID: "1",
    Name: "Activity 1",
    Kinds: ["Kind A"],
    Num: "10",
    DueDate: "2023-10-01",
  },
  {
    ActivityID: "1",
    Name: "Activity 2",
    Kinds: ["Kind B"],
    Num: "20",
    DueDate: "2023-10-15",
  },
  {
    ActivityID: "1",
    Name: "Activity 1",
    Kinds: ["Kind A"],
    Num: "10",
    DueDate: "2023-10-01",
  },
  {
    ActivityID: "1",
    Name: "Activity 2",
    Kinds: ["Kind B"],
    Num: "20",
    DueDate: "2023-10-15",
  },
  {
    ActivityID: "1",
    Name: "Activity 1",
    Kinds: ["Kind A"],
    Num: "10",
    DueDate: "2023-10-01",
  },
  {
    ActivityID: "1",
    Name: "Activity 2",
    Kinds: ["Kind B"],
    Num: "20",
    DueDate: "2023-10-15",
  },
  {
    ActivityID: "1",
    Name: "Activity 1",
    Kinds: ["Kind A"],
    Num: "10",
    DueDate: "2023-10-01",
  },
  {
    ActivityID: "1",
    Name: "Activity 2",
    Kinds: ["Kind B"],
    Num: "20",
    DueDate: "2023-10-15",
  },
  {
    ActivityID: "1",
    Name: "Activity 1",
    Kinds: ["Kind A"],
    Num: "10",
    DueDate: "2023-10-01",
  },
  {
    ActivityID: "1",
    Name: "Activity 2",
    Kinds: ["Kind B"],
    Num: "20",
    DueDate: "2023-10-15",
  },

]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = 10;
const AdminId = localStorage.getItem('AdminId');

const fetchActivities = async (page: number) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/search_activities?index=${currentPage.value}&page_size=${pageSize}`
    );
    activities.value = response.data.data;
    total.value = response.data.total;
  } catch (error) {
    console.error("Error fetching activities:", error);
  }
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchActivities(page);
};

onMounted(() => {
  fetchActivities(currentPage.value);
});
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  justify-content: flex-start;
  align-items: center;
  height: 700px;
}
.activity-card {
  margin-top: 100px; /* 添加一个margin-top，确保在导航栏下方 */
}
.pagination {
  height: 10px;
  padding: 16px;
  background-color: white;
  margin-top: 560px;
  /* position:fixed; */
}
.logout-button {
  position: absolute;
  bottom: 8px;
  right: 16px;
  padding: 8px 16px;
  margin-top: 560px;
  background-color: #071540d0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>