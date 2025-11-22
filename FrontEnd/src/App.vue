<template>
  <v-app>
    <v-main :class="['main-container', { 'photo-background': isPhotoBackPage }]">
      <div class='content-container'>
        <router-view class='router-view-container'/>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isPhotoBackPage = computed(() => route.path === '/register' 
|| route.path === '/find-password'
|| route.path === '/create-activity'
|| route.path === '/edituserinfo'
|| route.path === '/person');
</script>

<style scoped>
.main-container {
  display: flex;
}

.content-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.router-view-container {
  width: 1190px;
  height: 800px;
  padding: 20px;
  box-sizing: border-box;
  margin: auto 0;
}

.photo-background {
  background-image: url('/Logos/background.jpg'); /* 设置背景图片 */
  background-size: cover; /* 使背景图片覆盖整个区域 */
  background-position: center; /* 使背景图片居中 */
  background-repeat: no-repeat; /* 防止背景图片重复 */
  background-color: rgba(174, 206, 238, 0.613);
  /* background-color: rgba(238, 174, 202, 0.5186668417366946); 备用背景颜色 */
  background-blend-mode: multiply; /* 混合模式，使背景颜色与图片混合 */
}
</style>