<template>
    <div class="message" :class="messageClass">
      <img v-if="type === 'request'" src="@/assets/问号.svg" alt="question" style="margin-right: 20px;" />
      <img v-if="type === 'accept'" src="@/assets/对.svg" alt="accept" style="margin-right: 20px;" />
      <img v-if="type === 'reject'" src="@/assets/错误.svg" alt="reject" style="margin-right: 20px;" />
      <img v-if="type === 'move'" src="@/assets/移除.svg" alt="move" style="margin-right: 20px;" />
      <img v-if="type === 'quit'" src="@/assets/退出.svg" alt="quit" style="margin-right: 20px;" />
      <img v-if="type === 'break'" src="@/assets/解散.svg" alt="break" style="margin-right: 20px;" />
      <img v-if="type === 'delete'" src="@/assets/删除.svg" alt="delete" style="margin-right: 20px;" />
      <div class="message-content">
        <h3>{{ title }}</h3>
        <p v-if="type === 'request'" class="info">
            {{ name }} (ID: {{ id }}) 申请加入你的队伍
        </p>
        <p v-if="type === 'accept'" class="info">
            {{ name }} (ID: {{ id }}) 同意了你的组队请求
        </p>
        <p v-if="type === 'reject'" class="info">
            {{ name }} (ID: {{ id }}) 拒绝了你的组队请求
        </p>
        <p v-if="type === 'move'" class="info">
            {{ name }} (ID: {{ id }}) 将你移出队伍
        </p>
        <p v-if="type === 'quit'" class="info">
            {{ name }} (ID: {{ id }}) 已退出队伍
        </p>
        <p v-if="type === 'break'" class="info">
            {{ name }} (ID: {{ id }}) 已解散队伍
        </p>
        <p v-if="type === 'delete'" class="info">
            由于您的活动不符合社区规范，管理员已将该活动删除
        </p>
      </div>
      <div v-if="hasActions" class="actions">
        <div v-if="status === 'Unread' && type === 'request'">
          <button class="accept-btn" @click="Accept">同意</button>
          <button class="reject-btn" @click="Reject">拒绝</button>
          <button class="chat-btn"   @click="Chat">私聊 ></button>
        </div>
        <div v-if="status === 'Accept' && type === 'request'">
          <button class="accept-btn" disabled="true">已同意</button>
          <button class="chat-btn" @click="Chat">私聊 ></button>
        </div>
        <div v-if="status === 'Reject' && type === 'request'">
          <button class="reject-btn" disabled="true">已拒绝</button>
          <button class="chat-btn" @click="Chat">私聊 ></button>
        </div>
      </div>
      <span class="time">{{ time }}</span>
    </div>
  </template>

  <script>
  import axios from 'axios';
  import router from "@/router";

  export default {
    props: {
      type: {
        type: String,
        required: true,
        validator: function (value) {
          return ['request', 'accept', 'reject', 'move', 'quit', 'break', 'delete'].includes(value);
        }
      },
      title: {
        type: String,
        required: true
      },
      time: {
        type: String,
        required: true
      },
      name: {
        type: String,
        default: ''
      },
      id: {
        type: String,
        default: ''
      },
      m_id: {
        type: String,
        default: ''
      },
      status: {
        type: String,
        default: ''
      }
    },
    computed: {
      messageClass() {
        return `message-${this.type}`;
      },
      hasActions() {
        return this.type === 'request';
      }
    },
    methods: {
    async PostAccept() {
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/accept_message/`, {
            m_id: this.m_id
        });
        // 响应成功后的处理逻辑
        console.log('Request accepted:', response.message);
        // alert('已成功发送同意请求');
        this.$emit('refresh-data'); // 通知父组件刷新数据
        this.$emit('refresh-created-group');
      } catch (error) {
        // 处理错误
        console.error('Error accepting request:', error);
        alert('发送请求失败，请稍后重试');
      }
    },

    Accept() {
      console.log('按下了！！！');
      this.PostAccept();
    },

    async PostReject() {
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/reject_message/`, {
            m_id: this.m_id
        });
        // 响应成功后的处理逻辑
        console.log('Request accepted:', response.message);
        // alert('已成功发送同意请求');
        this.$emit('refresh-data'); // 通知父组件刷新数据
        this.$emit('refresh-created-group');
      } catch (error) {
        // 处理错误
        console.error('Error accepting request:', error);
        alert('发送请求失败，请稍后重试');
      }
    },

    Reject() {
      console.log('按下了！！！');
      this.PostReject();
    },

    Chat() {
      localStorage.setItem('activityName', this.title);
      localStorage.setItem('another_person', this.id);
      // activityId: localStorage.getItem('activityId')
      // userId: localStorage.getItem('userId')
      router.push('/chat-personal');
    },
  }
  };
  </script>

<style scoped>

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.info {
    font-size: small;
}

.message-content {
flex: 1;
}

.actions {
margin-left: auto;
}

.time {
    margin-left: auto;
color: #999;
font-size: 12px;
}

.accept-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
  background-color: #745b7a;
  color: white;
  font-size: small;
}

.reject-btn,
.chat-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 5px;
  font-size: small;
}

.chat-btn:hover {
  text-decoration: underline;
  /* 鼠标悬停时增加下划线 */
}

.reject-btn {
  background-color: #ded1e2;
  color: rgb(94, 94, 94);
}

.chat-btn {
  background-color: white;
  color: gray;
}
</style>
