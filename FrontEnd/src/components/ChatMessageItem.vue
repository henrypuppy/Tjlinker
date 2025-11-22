<template>
    <div class="message">
        <img :src="avatar" alt="avatar" style="margin-right: 20px; width: 50px; height: 50px" />

        <div class="message-content">
            <h3>{{ name }} (ID: {{ id }})</h3>
            <p class="info">
                {{ content }}
            </p>
        </div>

        <div class="actions">
            <div>
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
        avatar: {
            type: String,
            default: ''
            // required: true
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
        content: {
            type: String,
            default: ''
        },
        m_id: {
            type: String,
            default: ''
        },
    },
    methods: {
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
.info {
    font-size: small;
    color: gray;
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

.chat-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 5px;
  font-size: small;
  color: gray;
}

.chat-btn:hover {
  text-decoration: underline;
  /* 鼠标悬停时增加下划线 */
}
</style>
