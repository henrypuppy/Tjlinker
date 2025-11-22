<template>
  <div class="navbar">
    <!-- 左侧Logo和项目名称 -->
    <div class="navbar-left">
      <div @click="this.$router.push('/home')" style="cursor: pointer;">
        <img src='/Logos/Icon.png' style='width: 77px; border-radius: 30px;' alt='Icon'>
      </div>
      <img src='/Logos/Logo.png' style='width: 210px;' alt='Logo'>
    </div>

    <!-- 用户信息 -->
    <!-- <div v-if="localStorage.getItem('isAdmin') === 'no'"> -->
    <div class="navbar-user" @click="goToPersonPage">
      <img :src="avatar" alt="用户头像" class="user-icon" width="62px" height="60px" style="border-radius: 50%;" />
      <div class="user-info">
        <p>昵称: {{ nickname }}</p>
        <p>ID: {{ userId }}</p>
      </div>
    <!-- </div> -->
  </div>
  </div>
</template>

<script>
export default {
  props: {
    avatar: {
      type: String,
      default: '@/assets/性别-男.svg', // 使用 require 来保证路径解析
    },
    nickname: {
      type: String,
      default: '未知用户',
    },
    userId: {
      type: String,
      default: '00000000',
    },
  },
  data() {
    return {
    };
  },
  methods: {
    goToPersonPage() {
      // 跳转到/person页面
      this.$router.push('/person');
    },
  },
};
</script>

<style scoped>
/* 样式内容保持不变 */
.navbar {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
  position: fixed;
  top: 25px;
  left: 0;
  z-index: 1;
  background-color: #F5F5F5;
  width: 100%;
}

.navbar-left {
  display: flex;
  align-items: center;
  width: 400px;
  margin-left: 40px;
}

.navbar-user {
  display: flex;
  align-items: center;
  margin-left: 840px;
  background-color: #F5F5F5;
  border-radius: 30px;
  padding: 5px;
  width: 250px;
  height: 40px;
  cursor: pointer;
}

.user-info {
  margin-left: 15px;
}
</style>
