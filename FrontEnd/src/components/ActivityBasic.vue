<template>
    <div :style="positionStyle" class="activity-card">
      <div class="activity-info">
        <div class="left-column">
          <div class="Name">{{ Name }}</div>
          <div class="Kinds">
            <el-tag v-for="(Kind, index) in Kinds" :key="index" class="Kind">{{ Kind }}</el-tag>
          </div>
        </div>
        <div class="middle-column">
          <div class="Num">人数: {{ Num }}</div>
        </div>
        <div class="right-column">
          <div class="DueDate">截止时间: {{ DueDate }}</div>
          <!-- <a :href="DetailsLink" class="DetailsLink" target="_blank">查看详情 ></a> -->
          <button @click="goToDetails" class="DetailsLink">查看详情 》</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { computed } from 'vue'
  import { ElTag } from 'element-plus'
  import { useRouter } from "vue-router";
  const router = useRouter();
  
  const props = defineProps({
    Name: {
      type: String,
      required: true,
    },
    Kinds: {
      type: Array,
      required: true,
    },
    Num: {
      type: String,
      required: true,
    },
    DueDate: {
      type: String,
      default: 'auto',
    },
    ActivityID: {
      type: String,
      required: true,
    },
    top: {
      type: String,
      default: 'auto',
    },
    right: {
      type: String,
      default: 'auto',
    },
    bottom: {
      type: String,
      default: 'auto',
    },
    left: {
      type: String,
      default: 'auto',
    },
  })
  
  const positionStyle = computed(() => ({
    top: props.top,
    right: props.right,
    bottom: props.bottom,
    left: props.left,
  }))
  const goToDetails = () => {
    localStorage.setItem('activityId', props.ActivityID );
    if (localStorage.getItem('isAdmin') == 'no')
      router.push("/detail-activity");
    else router.push("/detail-activity-manager");
    // router.push({ name: "/detail-activity", params: { id: props.ActivityID } })
  }
  </script>
  
  <style scoped>
  .activity-card {
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
    height : 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .activity-info {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
  
  .left-column, .middle-column, .right-column {
    display: flex;
    flex-direction: column;
  }
  
  .left-column {
    flex: 1;
  }
  
  .middle-column {
    flex: 1;
    align-items: center;
  }
  
  .right-column {
    flex: 1;
    align-items: flex-end;
  }
  
  .Name {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .Kinds {
    display: flex;
    gap: 8px;
  }
  
  .Kind {
    margin: 0;
  }
  
  .Num {
    margin-top: 16px;
    font-size: 16px;
  }
  
  .DueDate {
    font-size: 16px;
    margin-bottom: 8px;
  }
  
  .DetailsLink {
    color: #409EFF;
    text-decoration: none;
  }
  </style>
  