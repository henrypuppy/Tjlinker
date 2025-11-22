<template>
  <div class="page-container">
    <div class="activity-card">
      <ActivityBasic
        v-for="(activity, index) in activities"
        :key="activity.ActivityID"
        :Name="activity.Name"
        :Kinds="activity.Kinds"
        :Num="activity.Num"
        :DueDate="activity.DueDate"
        :ActivityID="activity.ActivityID"
        :top="index % 2 === 0 ? `${index * 60 - 15}px` : `${(index-1) * 60 - 15}px`"
        :left="index % 2 === 0 ? '30px' : '680px'"
        :right="index % 2 === 0 ? '700px' : '30px'"
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
  </div>
</template>

<script setup lang='ts'>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import ActivityBasic from "@/components/ActivityBasic.vue"

const props = defineProps({
  firstCategory: {
    type: String,
    required: true
  },
  secondCategory: {
    type: String,
    required: true
  },
  searchKeyword: {
    type: String,
    required: false,
    default: ''
  },
  user_id: {
    type: String,
    required: true
  },
  currentMenu: {
    type: String,
    required: true
  }
});

const activities = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = 10

const fetchActivities = async (page: number, keyword: string, category: string, user_id: string, currentMenu: string) => {
  try {
    const url = currentMenu === '1' ? "http://127.0.0.1:8000/api/search_and_filter_activities/" : "http://127.0.0.1:8000/api/search_and_filter_dingyueactivities/";
    const params = {
      word: keyword,
      page: page.toString(),
      pageSize: pageSize.toString(),
      category: category,
      user_id: user_id
    };

    const queryParams = new URLSearchParams(params).toString();
    const encodedUrl = `${url}?${queryParams}`;

    const response = await axios.get(encodedUrl);
    if (response.data.success) {
      activities.value = response.data.data;
      total.value = response.data.total;
    } else {
      activities.value = [];
      total.value = 0;
    }
  } catch (error) {
    console.error('Error fetching activities:', error);
    activities.value = [];
    total.value = 0;
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchActivities(page, props.searchKeyword, getCategory(), props.user_id, props.currentMenu);
}

const getCategory = () => {
  if (props.firstCategory !== '' && props.secondCategory !== '') {
    return `${props.firstCategory},${props.secondCategory}`;
  } else if (props.firstCategory !== '') {
    return props.firstCategory;
  } else {
    return '全部';
  }
}

onMounted(() => {
  fetchActivities(currentPage.value, props.searchKeyword, getCategory(), props.user_id, props.currentMenu);
})

watch([() => props.firstCategory, () => props.secondCategory, () => props.searchKeyword, () => props.currentMenu], ([newFirstCategory, newSecondCategory, newSearchKeyword, newCurrentMenu]) => {
  fetchActivities(currentPage.value, newSearchKeyword, getCategory(), props.user_id, newCurrentMenu);
});
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 700px;
}

.pagination {
  height: 10px;
  padding: 16px; 
  margin-top: 600px;
  margin-right: 200px;
  justify-content: center;
}

.category-info {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}
</style>