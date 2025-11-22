<template>
  <div class="page-container">
    <el-page-header class="header" @back="goBack">
      <template #content>
        <span class="text"> 管理团队成员 </span>
      </template>
    </el-page-header>
    <div class="content-container">
      <div class="member-grid">
        <div v-for="member in members" :key="member.id" class="member-item">
          <img :src="member.avatar" alt="avatar" class="avatar" />
          <div class="member-info">
            <span class="member-id">{{ member.name }}</span>
            <el-checkbox v-model="member.selected"></el-checkbox>
          </div>
        </div>
      </div>
    </div>
    <el-button type="primary" class="deleteButton" @click="confirmDelete"
      >Delete</el-button
    >
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();

// 从本地存储获取活动ID
const activityId = ref(localStorage.getItem("activityId") || "");
// 定义成员列表
// const members = ref<
//   { id: string; name: string; avatar: string; selected: boolean }[]
// >([
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
//   { id: "123456", name: "aaa", avatar: "/Logos/Icon.png", selected: false },
// ]);
const members = ref<{ id: string; name: string; avatar: string; selected: boolean }[]>();
const goBack = () => {
  //router.push("/manage-team");
  router.go(-1);
};
// 页面加载时获取成员列表
onMounted(() => {
  fetchMembers();
});
// 获取成员列表
const fetchMembers = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/activity_members?activityId=${activityId.value}`
    );
    members.value = response.data.map((member) => ({
      ...member,
      selected: false,
    }));
  } catch (error) {
    console.error("Failed to fetch members:", error);
  }
};
const confirmDelete = () => {
  const selectedMembers = members.value.filter((member) => member.selected);
  if (selectedMembers.length === 0) {
    // ElMessageBox.alert("请选择要删除的成员", "提示", {
    //   confirmButtonText: "确定",
    // });
    alert("请选择要删除的成员");
    return;
  }

  // ElMessageBox.confirm("确定要移除当前所选成员吗？", "确认删除", {
  //   confirmButtonText: "确认",
  //   cancelButtonText: "取消",
  //   type: "warning",
  // })
  //   .then(() => {
  //     deleteMembers();
  //   })
  //   .catch(() => {
  //     // 用户取消删除
  //   });
  if(confirm("确定要移除当前所选成员吗？")){
    deleteMembers();
  }
};
// 删除成员
const deleteMembers = async () => {
  try {
    const selectedMemberIds = members.value
      .filter((member) => member.selected)
      .map((member) => member.id);

    // await axios.delete(`http://127.0.0.1:8000/api/delete_members?activityId=${activityId.value}`, {
    //   data: { memberIds: selectedMemberIds }
    // })
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/delete_members?activityId=${activityId.value}`,
      {
        data: { id: selectedMemberIds },
      }
    );
    if (response.status === 200) {
      // 从后端删除成功后，更新前端成员列表
      members.value = members.value.filter(
        (member) => !selectedMemberIds.includes(member.id)
      );
    } else {
      // ElMessageBox.alert("删除成员失败，请重试", "错误", {
      //   confirmButtonText: "确定",
      // });
      alert("删除成员失败，请重试");
    }
    // 从后端删除成功后，更新前端成员列表
    //members.value = members.value.filter(member => !selectedMemberIds.includes(member.id))
  } catch (error) {
    console.error("Failed to delete members:", error);
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  /* height: 100vh; */
  min-height: 100vh;
}

.text {
  color: white; /* 修改字体颜色 */
  font-size: 30px; /* 修改字体大小 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
.header {
  width: 100%;
  max-width: 1200px;
  max-height: 70px;
  height: 100%;
  margin-bottom: 20px;
  top: 0;
  margin-right: auto;
  background-color: #071540; /* 修改背景颜色 */
  color: white; /* 修改字体颜色 */
  border-radius: 10px; /* 设置圆角 */
  display: flex;
  justify-content: center; /* 水平居中 */
  position: fixed; /* 固定在页面底部 */
}
/* .deleteButton{
    position:fixed;
    bottom:0;
} */
.content-container {
  width: 100%;
  max-width: 1200px;
  margin-top: 90px; /* 为顶部留出空间 */
  flex-grow: 1; /* 使内容区域占据剩余空间 */
  overflow-y: auto; /* 使内容区域可以滚动 */
}
.deleteButton {
  position: fixed;
  bottom: 20px;
  width: 100%;
  max-width: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.member-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 每行五个成员 */
  gap: 20px; /* 成员之间的间距 */
}
.member-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}
.member-info {
  display: flex;
  align-items: center;
  justify-content: center;
}
.member-id {
  margin-right: 10px;
  font-size: 16px;
}
</style>
