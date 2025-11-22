<template>
  <div>
    <!-- 调用导航栏组件 -->
    <TopNavBar :avatar="user.avatarUrl" :nickname="user.username" :userId="user.id"
      @update:searchKeyword="handleSearchUpdate" @search="handleSearchSubmit" />

    <div class="page-container">

      <div class="page-left" style="border: 1px solid #ccc;border-radius: 20px; ">
        <aside class="menu">
          <el-menu active-text-color=" rgb(0, 106, 255)" background-color="#fff" class="el-menu-vertical-demo"
            default-active="1" text-color="#000" @open="handleOpen" @close="handleClose" @select="handleMenuSelect">
            <el-menu-item index="1" style="border: 1px solid #ccc;">
              <span style="font-size: 25px; ">首页</span>
            </el-menu-item>
            <el-menu-item index="2" style="border: 1px solid #ccc;">
              <span style="font-size: 25px; ">订阅</span>
            </el-menu-item>
          </el-menu>
        </aside>
      </div>

      <div class="page-right">

        <div class="label-container">
          <div class="label-left">
            <div class="label-top">
              <p style="margin-bottom:10px">
                {{ currentMenu === '1' ? '当前活动类目：' : '您订阅的类目：' }} {{ selectedCategory.first }} - {{ selectedCategory.second }}
              </p>

              <template v-if="currentMenu === '1' && selectedCategory.first !== '全部'">
                <ImageButton :imageSrc="isSubscribed ? '/Logos/dingyue1.png' : '/Logos/dingyue0.png'" altText="Example Image" width="20px"
                  height="20px" @click="handleDingYue" />
              </template>
            </div>

            <div class="label-list">
              <!-- <el-dropdown v-if="currentMenu === '1'" placement="bottom" @command="handleCommand" style="margin-right:30px">
                <el-button @click="handleAllclick">全部</el-button>
              </el-dropdown> -->

              <el-dropdown  placement="bottom" @command="handleCommand" style="margin-right:30px">
                <el-button @click="handleAllclick">全部</el-button>
              </el-dropdown>



              <div v-for="firstCategory in categories" :key="firstCategory.first" class="first-category">
                <el-dropdown placement="bottom" style="margin-right:30px">
                  <el-button @click="handleFirstClassclick(firstCategory.first)">{{ firstCategory.first }}</el-button>
                  <template v-if="firstCategory.first !== '其他' && firstCategory.second.length > 0" #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-for="secondCategory in firstCategory.second" :key="secondCategory.classID"
                        @click="handleSecondCategoryClick(firstCategory.first, secondCategory.classname)">
                        {{ secondCategory.classname }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>

          </div>

          <div class="label-right" style="margin-left:880px; margin-top: 20px;">
            
            <ImageButton url="/create-activity" imageSrc="/Logos/add.png" altText="Example Image" width="50px"
              height="50px" @click="router.push('/create-activity')" />
          </div>

        </div>

        <div class="activity-container">
          <ActivityList :firstCategory="selectedCategory.first" :secondCategory="selectedCategory.second"
            :searchKeyword="searchKeyword" :user_id="user.id" :currentMenu="currentMenu" />
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import TopNavBar from '@/components/TopNavBar.vue';
import ActivityList from '@/components/ActivityList.vue';
import ImageButton from '@/components/ImageButton.vue'; // 确保你有一个 ImageButton 组件
import { useRouter } from 'vue-router'
const router = useRouter()

const user = ref({
  username: '111',
  avatarUrl: '',
  id: localStorage.getItem('userId'),
});

const searchKeyword = ref('');
const submittedKeyword = ref('');
const categories = ref([]);
const selectedCategory = ref({ first: '全部', second: '' }); // 修改为对象
const isSubscribed = ref(false); // 订阅状态
const currentMenu = ref('1'); // 当前选择的菜单项

const fetchUserData = async () => {
  const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
  const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    user.value = {
      username: data.Name,
      avatarUrl: data.Avatar, // 获取头像的URL
      id: userId
    };
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};

const fetchCategories = async (menu) => {
  const apiUrl = menu === '1' ? 'http://127.0.0.1:8000/api/get_class/' : 'http://127.0.0.1:8000/api/get_dingyue_class/';
  const params = menu === '2' ? { user_id: user.value.id } : {};
  try {
    const response = await fetch(`${apiUrl}?${new URLSearchParams(params).toString()}`);
    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        categories.value = data.data;
      } else {
        console.error('Failed to fetch categories:', data.message);
      }
    } else {
      console.error('Failed to fetch categories:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

const fetchSubscriptionStatus = async (first, second) => {
  const category = second ? `${first},${second}` : first;
  const url = `http://127.0.0.1:8000/api/check_subscription_status/`;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user.value.id,
        category: category,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    if (data.success) {
      isSubscribed.value = data.isSubscribed; // 更新订阅状态
    } else {
      console.error('Failed to fetch subscription status:', data.message);
    }
  } catch (error) {
    console.error('Error fetching subscription status:', error);
  }
};

const handleSearchUpdate = (newKeyword) => {
  // 实时更新搜索内容
  searchKeyword.value = newKeyword;
};

const handleSearchSubmit = (finalKeyword) => {
  // 处理提交的搜索内容
  submittedKeyword.value = finalKeyword;
  // 可以在此执行搜索逻辑
  console.log("执行搜索:", finalKeyword);
};

const handleCommand = (command) => {
  selectedCategory.value = { first: command, second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus(command, ''); // 获取订阅状态
};

const handleAllclick = () => {
  selectedCategory.value = { first: '全部', second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus('全部', ''); // 获取订阅状态
};

const handleFirstClassclick = (first) => {
  selectedCategory.value = { first: first, second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus(first, ''); // 获取订阅状态
};

const handleSecondCategoryClick = (first, second) => {
  selectedCategory.value = { first, second }; // 更新选中的二级类目ID
  fetchSubscriptionStatus(first, second); // 获取订阅状态
};

const handleDingYue = async () => {
  const category = selectedCategory.value.second ? `${selectedCategory.value.first},${selectedCategory.value.second}` : selectedCategory.value.first;
  const url = isSubscribed.value ? 'http://127.0.0.1:8000/api/unsubscribe_category/' : 'http://127.0.0.1:8000/api/subscribe_category/';
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user.value.id,
        category: category,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    if (data.success) {
      isSubscribed.value = !isSubscribed.value; // 切换订阅状态
    } else {
      console.error('Failed to handle subscription:', data.message);
    }
  } catch (error) {
    console.error('Error handling subscription:', error);
  }
};

const handleMenuSelect = (index) => {
  currentMenu.value = index;
  fetchCategories(index);
};

onMounted(() => {
  fetchUserData();
  fetchCategories(currentMenu.value);
  fetchSubscriptionStatus('全部', ''); // 初始化订阅状态
});

watch([() => selectedCategory.value.first, () => selectedCategory.value.second], ([newFirst, newSecond]) => {
  fetchSubscriptionStatus(newFirst, newSecond); // 监听类目变化并获取订阅状态
});
</script>

<style scoped>
/* 父组件样式 */

.page-container {
  display: flex;
  flex-direction: row;
  margin-top: 60px;
}

.page-left {
  position: relative;
  position: fixed;
  top: 115px;
  left: 0px;
  width: 150px;
  height: 900px;
}

.page-right {
  position: relative;
  position: fixed;
  top: 125px;
  left: 170px;
  width: 1500px;
  height: 900px;
}

.label-container {
  display: flex;
  flex-direction: row;
}

.label-list {
  display: flex;
  flex-direction: row;
}

.label-top{
  display: flex;
  flex-direction: row;

}

.activity-container {
  position: relative;
}

.label-right{
  position:fixed;
}

.el-menu--border-card>>>.el-menu__item.is-active {
  background-color: var(--el-menu-active-color);
}

::v-deep .el-menu-item.is-active {
  background-color: #ECF5FF; /* 设置背景颜色为激活颜色 */
}

::v-deep .el-menu-item {
  border-radius: 10px;

}
</style>