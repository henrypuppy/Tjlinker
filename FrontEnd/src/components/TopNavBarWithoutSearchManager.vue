<template>
  <div class="navbar">
    <!-- 左侧Logo和项目名称 -->
    <div class="navbar-left">
      <div @click="this.$router.push('/manager')" style="cursor: pointer;">
        <img src='/Logos/Icon.png' style='width: 77px; border-radius: 30px;' alt='Icon'>
      </div>
      <img src='/Logos/Logo.png' style='width: 210px;' alt='Logo'>
    </div>

    <!-- 用户信息 -->
    <!-- <div v-if="localStorage.getItem('isAdmin') === 'no'"> -->
    <div class="navbar-manager">
      <!-- <img :src="avatar" alt="管理员头像" class="manager-icon" width="62px" height="60px" style="border-radius: 50%;" /> -->
      <div class="manager-info">
        <p>你好，管理员~</p>
        <p>ID: {{ AdminId }}</p>
      </div>
    <!-- </div> -->
  </div>
  </div>
</template>

<script>
export default {
  props: {
    AdminId: {
      type: String,
      default: '000',
    },
  },
  data() {
    return {

    };
  },
  methods: {
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

.navbar-manager {
  display: flex;
  align-items: center;
  margin-left: 840px;
  background-color: #F5F5F5;
  border-radius: 30px;
  padding: 5px;
  width: 250px;
  height: 40px;
}

.manager-info {
  margin-right: 30px;
}
</style>
