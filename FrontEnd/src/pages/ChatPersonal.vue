<template>
  <div class="page-container">
    <el-page-header :icon="ArrowLeft" class="header" @back="goBack">
      <template #content>
        <span class="text"> {{ ReceiveUserName }} </span>
      </template>
    </el-page-header>
    <div
      v-for="(message, index) in chatMessages"
      :key="index"
      :class="message.WhetherCurrent === true ? 'data3' : 'data'"
    >
      <img
        v-if="message.WhetherCurrent === false"
        :src="ReceiveUserAvatarUrl"
        width="50"
        height="50"
        class="user"
      />
      <el-text class="messagetext" size="large">{{ message.Message }}</el-text>
      <img
        v-if="message.WhetherCurrent === true"
        :src="SendUserAvatarUrl"
        width="50"
        height="50"
        class="user"
      />
    </div>

    <div class="bottom-input">
      <el-input
        v-model="input"
        style="width: 1150px"
        placeholder="请输入消息"
        size="large"
        @keydown="handleInputKeydown"
      />
    </div>
  </div>
</template>

<script setup lang='ts'>
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios"; // 假设你使用 axios 进行 HTTP 请求
import { useRouter } from "vue-router";
const router = useRouter();

const chatMessages = ref<
  { WhetherCurrent: boolean; Message: string; Timestamp: string }[]
>([]); // 存储聊天记录
const input = ref(""); // 输入框的内容
const page = ref(1); // 当前页码
const isLoading = ref(false); // 是否正在加载数据

const SendUserID = ref(localStorage.getItem("userId") || ""); // 从 localStorage 获取sender用户 ID
const SendUserAvatarUrl = ref("/Logos/Icon.png"); // 初始化，fetch获取sender用户头像
const ReceiveUserID = ref(localStorage.getItem("another_person") || ""); // 从 localStorage 获取receive用户 ID（暂时写死）
const ReceiveUserName = ref("这是Receive"); //初始化，fetch获取receive用户头像
const ReceiveUserAvatarUrl = ref("/Logos/Icon.png"); // 初始化，fetch获取receive用户头像

const initialTimestamp = ref("");
const currentTimestamp = ref(""); // 存储当前时间戳
let intervalId: number; // 用于存储定时器的 ID
let isFetching = false; // 锁标志

const goBack = () => {
  //router.push("/manage-team");
  router.go(-1);
};
// 初始化部分
// 组件挂载和删除
onMounted(() => {
  window.addEventListener("scroll", handleScroll);
  intervalId = setInterval(fetchLatestMessages, 5000);
  initialTimestamp.value = new Date().toISOString(); //当前时间戳
  currentTimestamp.value = initialTimestamp.value;

  fetchSendUserAvatarUrl(); // 获取当前用户的头像
  fetchReceiveUserAvatarUrl(); // 获取当前用户的头像
  fetchChatMessages(page.value); // 初始加载第一页数据
  scrollToBottom();
});
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  clearInterval(intervalId); // 清除定时器
});
//获取当前用户头像
const fetchSendUserAvatarUrl = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/users/info?id=${SendUserID.value}`
    );
    SendUserAvatarUrl.value = response.data.Avatar;
  } catch (error) {
    console.error("Error fetching current user ID:", error);
  }
};
const fetchReceiveUserAvatarUrl = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/users/info?id=${ReceiveUserID.value}`
    );
    ReceiveUserAvatarUrl.value = response.data.Avatar;
    ReceiveUserName.value = response.data.Name;
  } catch (error) {
    console.error("Error fetching current user ID:", error);
  }
};

// 聊天记录部分
// 后端请求
const fetchChatMessages = async (pageNumber: number) => {
  if (isFetching) return; // 如果正在请求，直接返回
  isFetching = true; // 加锁
  try {
    isLoading.value = true;
    const response = await axios.get(
      `http://127.0.0.1:8000/api/get_chat_messages_personal/?SendUserID=${SendUserID.value}&ReceiveUserID=${ReceiveUserID.value}&page=${pageNumber}&initialTimestamp=${initialTimestamp.value}`
    );
    chatMessages.value.unshift(...response.data.messages); // 将新数据添加到现有数据的开头 -->
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching chat messages:", error);
    isLoading.value = false;
  } finally {
    isFetching = false; // 解锁
  }
};

// 滚动事件监听
const handleScroll = () => {
  const scrollTop = document.documentElement.scrollTop;
  if (scrollTop === 0 && !isLoading.value) {
    // 滚动到顶部时，请求上一页数据
    page.value += 1;
    fetchChatMessages(page.value);
  }
};

// 发送消息部分
const sendMessage = async () => {
  if (input.value.trim() === "") return; // 如果输入为空，不发送消息

  const newMessage = {
    Message: input.value,
    SendUserID: SendUserID.value,
    ReceiveUserID: ReceiveUserID.value,
    Timestamp: new Date().toISOString(),
  };

  // 将消息添加到前端的聊天记录中
  //chatMessages.value.push(newMessage);
  // 清空输入框
  input.value = "";

  // 将消息发送给后端
  try {
    await axios.post(
      "http://127.0.0.1:8000/api/send_message_personal/",
      newMessage
    );
  } catch (error) {
    console.error("Error sending message:", error);
  }
};

// enter时间监听
const handleInputKeydown = (event: KeyboardEvent) => {
  if (event.key === "Enter") {
    sendMessage();
  }
};

// 获取当前最新消息
const fetchLatestMessages = async () => {
  if (isFetching) return; // 如果正在请求，直接返回
  isFetching = true; // 加锁
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/get_latest_messages_personal/?SendUserID=${SendUserID.value}&ReceiveUserID=${ReceiveUserID.value}&currentTimestamp=${currentTimestamp.value}`
    ); // 假设后端接口为 /api/chat/latest
    const newMessages = response.data.messages;

    // 将新消息添加到聊天记录中
    if (newMessages.length > 0) {
      chatMessages.value.push(...newMessages);
      // 更新 nowTimestamp
      currentTimestamp.value = newMessages[newMessages.length - 1].Timestamp;
      scrollToBottom();
    }
  } catch (error) {
    console.error("Error fetching latest messages:", error);
  } finally {
    isFetching = false; // 解锁
  }
};

// 滚动到页面底部的函数
const scrollToBottom = () => {
  setTimeout(() => {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: "smooth",
    });
  }, 100); // 延迟 100ms 以确保 DOM 更新
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  overflow-y: auto; /* 允许垂直滚动 */
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

.text {
  color: white; /* 修改字体颜色 */
  font-size: 30px; /* 修改字体大小 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
.data {
  width: 100%;
  max-width: 600px;
  height: 100%;
  max-height: 70px;
  margin-top: 20px; /* 设置一个固定的间距 */
  font-size: 50px; /* 修改字体大小 */
  margin-right: auto;
  display: flex;
}
.data2 {
  width: 100%;
  max-width: 600px;
  height: 100%;
  max-height: 70px;
  margin-top: 20px; /* 设置一个固定的间距 */
  font-size: 50px; /* 修改字体大小 */
  margin-right: auto;
  display: flex;
}
.data3 {
  width: 100%;
  max-width: 600px;
  height: 100%;
  max-height: 70px;
  margin-top: 20px; /* 设置一个固定的间距 */
  font-size: 50px; /* 修改字体大小 */
  margin-left: auto;
  display: flex;
  justify-content: flex-end; /* 子元素右对齐 */
}
.messagetext {
  display: flex;
  align-items: center; /* 垂直居中 */
  margin-bottom: auto;
  padding: 10px;
  font-size: 24px; /* 修改字体大小 */
  border: 1px solid var(--el-border-color);
  border-radius: var(--el-border-radius-base);
}
.user {
  display: flex;
  margin-right: 15px; /* 增加头像和文本之间的间距 */
  margin-left: 15px; /* 增加头像和文本之间的间距 */
}
.large-radius {
  height: auto;
  width: 100%;
  max-width: 1700px;
  bottom: 0; /* 距离底部 0 */
  border: 1px solid var(--el-border-color);
  border-radius: var(--el-border-radius-base);
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.bottom-input {
  position: fixed; /* 固定在页面底部 */
  bottom: 20px; /* 距离底部 20px */
  left: 50%; /* 水平居中 */
  bottom: 0;
  transform: translateX(-50%); /* 修正水平居中偏移 */
  width: 100%; /* 设置宽度 */
  max-width: 1150px; /* 最大宽度 */
  padding: 0 15px; /* 保持页面两边留白 */
  box-sizing: border-box; /* 确保 padding 不影响宽度 */
}
</style>
