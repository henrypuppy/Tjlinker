<template>
  <div class="centered-container">
    <!-- <TopNavBarWithoutSearch :avatar="user.avatarUrl" :nickname="user.username" :userId="user.id" /> -->
    <!-- <TopNavBarWithoutSearch :avatar="user.avatarUrl" :nickname="user.username" :userId="user.id" /> -->

    <el-page-header :icon="ArrowLeft" class="header" @back="goBack">
      <template #content>
        <span class="text"> 活动创建 </span>
      </template>
    </el-page-header>
    <div class="large-radius">
      <div class="page-container">
        <el-form
          ref="ruleFormRef"
          style="max-width: 1700px"
          :model="ruleForm"
          :rules="rules"
          label-width="auto"
          class="demo-ruleForm"
          :size="formSize"
          status-icon
          :label-position="labelPosition"
        >
          <el-form-item label="活动名称" prop="Name">
            <el-input v-model="ruleForm.Name" />
          </el-form-item>

          <el-form-item label="活动所在校区" prop="RegionKind">
            <el-select v-model="ruleForm.RegionKind">
              <el-option label="四平路校区" value="四平路校区" />
              <el-option label="嘉定校区" value="嘉定校区" />
              <el-option label="沪西校区" value="沪西校区" />
              <el-option label="沪北校区" value="沪北校区" />
              <el-option label="校外" value="校外" />
            </el-select>
          </el-form-item>

          <el-form-item label="活动详细地点" prop="RegionDetailed">
            <el-input v-model="ruleForm.RegionDetailed" />
          </el-form-item>

          <el-form-item label="活动所属类目" prop="Kind">
            <el-cascader v-model="ruleForm.Kind" :options="Options" clearable />
          </el-form-item>

          <el-form-item label="活动时间" required="True">
            <el-col :span="11">
              <el-form-item prop="Date1">
                <el-date-picker v-model="ruleForm.Date1" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col class="text-center" :span="2">
              <span class="text-gray-500">-</span>
            </el-col>
            <el-col :span="11">
              <el-form-item prop="Time1">
                <el-time-picker v-model="ruleForm.Time1" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-form-item>

          <el-form-item label="报名截止时间" required="True">
            <el-col :span="11">
              <el-form-item prop="Date2">
                <el-date-picker v-model="ruleForm.Date2" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col class="text-center" :span="2">
              <span class="text-gray-500">-</span>
            </el-col>
            <el-col :span="11">
              <el-form-item prop="Time2">
                <el-time-picker v-model="ruleForm.Time2" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-form-item>

          <el-form-item label="是否期望与参与者互通实名" prop="RealName">
            <el-radio-group v-model="ruleForm.RealName">
              <el-radio value="true">是</el-radio>
              <el-radio value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="活动人数限额" prop="Num">
            <el-input-number
              v-model="ruleForm.Num"
              :min="1"
              :max="100"
              @change="handleChange"
            />
          </el-form-item>

          <el-form-item label="活动详情" prop="Detailed">
            <el-input v-model="ruleForm.Detailed" type="textarea" />
          </el-form-item>

          <el-form-item style="margin-left: 450px">
            <el-button type="primary" @click="submitForm(ruleFormRef)"
              >创建</el-button
            >
            <el-button @click="resetForm(ruleFormRef)">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>


<script setup lang='ts'>
import { reactive, ref } from "vue";
import type {
  ComponentSize,
  FormInstance,
  FormRules,
  FormProps,
} from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();

interface RuleForm {
  Creator: string;
  Name: string;
  RegionKind: string;
  RegionDetailed: string;
  Kind: string;
  Date1: string;
  Time1: string;
  Date2: string;
  Time2: string;
  RealName: boolean;
  Num: number;
  Detailed: string;
}

const formSize = ref<ComponentSize>("large");
const ruleFormRef = ref<FormInstance>();
const labelPosition = ref<FormProps["labelPosition"]>("right");
const ruleForm = reactive<RuleForm>({
  Creator: localStorage.getItem("userId") || "",
  Name: "",
  RegionKind: "",
  RegionDetailed: "",
  Kind: "",
  Date1: "",
  Time1: "",
  Date2: "",
  Time2: "",
  RealName: false,
  Num: 100,
  Detailed: "",
});

const rules = reactive<FormRules<RuleForm>>({
  Name: [
    {
      required: true,
      message: "请输入活动名称",
      trigger: "blur",
    },
    {
      validator: (rule, value, callback) => {
        if (value.length > 10) {
          callback(new Error("活动名称不能超过10个字"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  RegionKind: [
    {
      required: true,
      message: "请选择活动校区",
      trigger: "change",
    },
  ],
  RegionDetailed: [
    {
      required: true,
      message: "请输入活动详细地点",
      trigger: "blur",
    },
  ],
  Kind: [
    {
      required: true,
      message: "请选择活动类目",
      trigger: "change",
    },
  ],
  Date1: [
    {
      required: true,
      message: "请选择活动日期",
      trigger: "change",
    },
  ],
  Time1: [
    {
      required: true,
      message: "请选择活动时间",
      trigger: "change",
    },
  ],
  Date2: [
    {
      required: true,
      message: "请选择报名截止日期",
      trigger: "change",
    },
  ],
  Time2: [
    {
      required: true,
      message: "请选择报名截止时间",
      trigger: "change",
    },
  ],
  Detailed: [
    {
      required: true,
      message: "请输入活动详情",
      trigger: "blur",
    },
  ],
});

// const submitForm = async (formEl: FormInstance | undefined) => {
//   if (!formEl) return;

//   formEl.validate((valid, fields) => {
//     if (valid) {
//       const url = "http://127.0.0.1:8000/api/create_activities/"; // 替换为你的后端API端点
//       console.log("Sending request to:", url); // 打印请求URL

//       // 构建要提交的数据对象
//       const formData = {
//         CreatorID: ruleForm.Creator, // 你可能需要根据实际情况获取创建者信息
//         Name: ruleForm.Name,
//         Campus_search_for_ID: ruleForm.RegionKind,
//         Location: ruleForm.RegionDetailed,
//         Class_search_for_ID1: ruleForm.Kind[0],
//         Class_search_for_ID2: ruleForm.Kind[1],
//         StartDate: ruleForm.Date1 + ruleForm.Time1,
//         DueDate: ruleForm.Date2 + ruleForm.Time2,
//         NeedRealName: ruleForm.RealName,
//         NumLimit: ruleForm.Num,
//         Description: ruleForm.Detailed,
//       };

//       // 发送请求到后端创建活动
//       fetch(url, {
//         method: "POST", // 确保使用POST请求
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(formData),
//       })
//         .then((response) => {
//           if (!response.ok) {
//             throw new Error("活动创建失败，请稍后再试");
//           }
//           return response.json();
//         })
//         .then((data) => {
//           console.log("Activity created successfully:", data);
//           // 处理创建成功后的逻辑
//           alert("活动创建成功！");
//           router.push("/home");
//         })
//         .catch((error) => {
//           console.error("Error creating activity:", error);
//           // 处理创建错误后的逻辑
//           alert("活动创建失败，请检查表单数据并重试。");
//         });
//     } else {
//       console.log("error submit!");
//     }
//   });
// };
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  formEl.validate(async (valid, fields) => {
    if (valid) {
      const url = "http://127.0.0.1:8000/api/create_activities/"; // 后端API端点
      console.log("Sending request to:", url);

      const formData = {
        CreatorID: ruleForm.Creator,
        Name: ruleForm.Name,
        Campus_search_for_ID: ruleForm.RegionKind,
        Location: ruleForm.RegionDetailed,
        Class_search_for_ID1: ruleForm.Kind[0],
        Class_search_for_ID2: ruleForm.Kind[1],
        StartDate: ruleForm.Date1 + ruleForm.Time1,
        DueDate: ruleForm.Date2 + ruleForm.Time2,
        NeedRealName: ruleForm.RealName,
        NumLimit: ruleForm.Num,
        Description: ruleForm.Detailed,
      };

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Activity created successfully:", data);
          alert("活动创建成功！");
          router.push("/home");
        } else {
          if (response.status === 405) {
            // rules.Date2[1] = {
            //   validator: (rule, value, callback) => {
            //     callback(new Error("报名截止时间需在活动时间之前")); // 显示后端返回的错误信息
            //   },
            //   trigger: "change",
            // };
            // formEl.validate(); // 触发重新验证
            alert("报名截止时间需在活动时间之前");
            
          } else {
            throw new Error("活动创建失败，请稍后再试");
          }
        }
      } catch (error) {
        console.error("Error creating activity:", error);
        alert("活动创建失败，请检查表单数据并重试。");
      }
    } else {
      console.log("error submit!");
      formEl.validate(); // 触发重新验证
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};

const Options = [
  {
    value: "科研竞赛",
    label: "科研竞赛",
    children: [
      {
        value: "竞赛组队",
        label: "竞赛组队",
      },
      {
        value: "项目组招募",
        label: "项目组招募",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "学习互助",
    label: "学习互助",
    children: [
      {
        value: "考研",
        label: "考研",
      },
      {
        value: "考公",
        label: "考公",
      },
      {
        value: "留学",
        label: "留学",
      },
      {
        value: "语言学习",
        label: "语言学习",
      },
      {
        value: "实习",
        label: "实习",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "体育活动",
    label: "体育活动",
    children: [
      {
        value: "羽毛球",
        label: "羽毛球",
      },
      {
        value: "乒乓球",
        label: "乒乓球",
      },
      {
        value: "网球",
        label: "网球",
      },
      {
        value: "足球",
        label: "足球",
      },
      {
        value: "排球",
        label: "排球",
      },
      {
        value: "篮球",
        label: "篮球",
      },
      {
        value: "游泳",
        label: "游泳",
      },
      {
        value: "跑步",
        label: "跑步",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "娱乐组局",
    label: "娱乐组局",
    children: [
      {
        value: "演唱会",
        label: "演唱会",
      },
      {
        value: "旅行",
        label: "旅行",
      },
      {
        value: "电影",
        label: "电影",
      },
      {
        value: "KTV",
        label: "KTV",
      },
      {
        value: "剧本杀",
        label: "剧本杀",
      },
      {
        value: "密室逃脱",
        label: "密室逃脱",
      },
      {
        value: "美食探店",
        label: "美食探店",
      },
      {
        value: "CityWalk",
        label: "CityWalk",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "拼车出行",
    label: "拼车出行",
    children: [
      {
        value: "嘉定校区",
        label: "嘉定校区",
      },
      {
        value: "四平路校区",
        label: "四平路校区",
      },
      {
        value: "沪西校区",
        label: "沪西校区",
      },
      {
        value: "沪北校区",
        label: "沪北校区",
      },
      {
        value: "彰武校区",
        label: "彰武校区",
      },
      {
        value: "铁岭校区",
        label: "铁岭校区",
      },
    ],
  },
  {
    value: "同薅羊毛",
    label: "同薅羊毛",
    children: [
      {
        value: "互助点赞",
        label: "互助点赞",
      },
      {
        value: "拼单团购",
        label: "拼单团购",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "其他",
    label: "其他",
  },
];

// const num = ref(1);
const handleChange = (value: number) => {
  console.log(value);
};

// const user = ref({
//   username: '111',
//   avatarUrl: '',
//   id: localStorage.getItem('userId'),
// });
// const fetchUserData = async () => {
//   const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
//   const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中
//   try {
//     const response = await fetch(url, {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         // 如果需要，可以在这里添加认证信息，例如：
//         // 'Authorization': 'Bearer your-token'
//       },
//     });

//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }

//     const data = await response.json();
//     user.value = {
//       username: data.Name,
//       avatarUrl: data.Avatar, // 获取头像的URL
//       id: userId
//     };
//   } catch (error) {
//     console.error('There was a problem with the fetch operation:', error);
//   }
// };

// onMounted(() => {
//   fetchUserData();
// });
const goBack = () => {
  router.push("/home");
  console.log("go back");
};
</script>

<style scoped>
/* .centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.page-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.large-radius {
  height: 300px;
  width: 500px;
  border: 1px solid var(--el-border-color);
  border-radius: var(--el-border-radius-base);
} */
.centered-container {
  justify-content: center;
  align-items: center;
  height: 100vh; /* 使容器占满整个视口高度 */
}

.large-radius {
  background-color: white;
  height: auto;
  width: 100%;
  max-width: 1700px;
  border: 1px solid var(--el-border-color);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.header {
  width: 100%;
  max-width: 1200px;
  max-height: 50px;
  height: 100%;
  margin-bottom: 20px;
  margin-right: auto;
  background-color: #071540d0; /* 修改背景颜色 */
  color: white; /* 修改字体颜色 */
  border-radius: 10px; /* 设置圆角 */
  display: flex;
  justify-content: center; /* 水平居中 */
}
.text {
  color: white; /* 修改字体颜色 */
  font-size: 30px; /* 修改字体大小 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
.page-container {
  width: 100%;
}
</style>