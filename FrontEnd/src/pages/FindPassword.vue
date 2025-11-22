<!-- 逻辑完全实现，只差页面修改 -->

<template>
  <div class="image-container">
    <img src='/Logos/FindPasswordTitle.png' alt="title" class="full-width-image" />
  </div>
  <div class='page-container'>
    <v-app>
      <v-container>
        <div class="card">

        <v-stepper v-model="currentStep" mobile>
          <v-stepper-header>
            <template v-for="(item, i) in items" :key="i">
              <v-divider v-if="i"></v-divider>
              <v-stepper-item :value="item.value" :title="item.title" :subtitle="item.subtitle"></v-stepper-item>
            </template>
          </v-stepper-header>

          <v-stepper-items>
            <!-- 第一步：输入用户ID和三个密码问题 -->
            <v-stepper-content v-if="currentStep === 1" :step="1">
              <v-card class="custom-card" title="验证用户信息" flat>
                <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" status-icon :rules="rules"
                  label-width="auto" class="demo-ruleForm">

                  <el-form-item label="用户ID" prop="userId">
                    <el-input v-model="ruleForm.userId" type="text" autocomplete="off" />
                  </el-form-item>

                  <el-form-item label="您的出生地是" prop="question1">
                    <el-input v-model="ruleForm.question1" type="text" autocomplete="off" />
                  </el-form-item>

                  <el-form-item label="您父亲的姓名是" prop="question2">
                    <el-input v-model="ruleForm.question2" type="text" autocomplete="off" />
                  </el-form-item>

                  <el-form-item label="您母亲的姓名是" prop="question3">
                    <el-input v-model="ruleForm.question3" type="text" autocomplete="off" />
                  </el-form-item>

                  <el-form-item style="margin-left: 220px;margin-top: 30px">
                    <el-button type="primary" @click="submitForm(ruleFormRef)">
                      提交
                    </el-button>
                    <el-button @click="resetForm(ruleFormRef)">重置</el-button>
                  </el-form-item>
                </el-form>
              </v-card>
            </v-stepper-content>

            <!-- 第二步：修改密码 -->
            <v-stepper-content v-if="currentStep === 2" :step="2">
              <v-card class="custom-card" title="修改密码（请输入8-20位数字或字母）" flat>
                <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" status-icon :rules="rules"
                  label-width="auto" class="demo-ruleForm">
                  <el-form-item label="新密码" prop="newPassword">
                    <el-input v-model="ruleForm.newPassword" type="password" autocomplete="off" />
                  </el-form-item>

                  <el-form-item label="确认新密码" prop="confirmPassword">
                    <el-input v-model="ruleForm.confirmPassword" type="password" autocomplete="off" />
                  </el-form-item>

                  <el-form-item style="margin-left: 220px;margin-top: 30px">
                    <el-button type="primary" @click="submitForm(ruleFormRef)">
                      提交
                    </el-button>
                    <el-button @click="resetForm(ruleFormRef)">返回上一步</el-button>
                  </el-form-item>
                </el-form>
              </v-card>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>

      </div>

        <div class='button-container'>
          <WhiteButton width='150px' height='40px' style='margin-left: 0px' @click="router.push('/login/user')">
            <p style='font-size: 15px'>返回用户登录界面</p>
          </WhiteButton>

        </div>




      </v-container>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
import { ref, reactive } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';

const ruleFormRef = ref<FormInstance>();
const currentStep = ref(1); // 当前步骤
const stepperKey = ref(0);  // 用于强制刷新 v-stepper

// 动态步骤数据
const items = ref(Array.from({ length: 2 }).map((_, i) => ({
  title: `Step ${i + 1}`,
  subtitle: `Step ${i + 1} subtitle`,
  value: i + 1,
})));

// 表单数据和校验规则
const ruleForm = reactive({
  userId: '',
  question1: '',
  question2: '',
  question3: '',
  newPassword: '',
  confirmPassword: ''
});

const rules = reactive<FormRules<typeof ruleForm>>({
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  question1: [{ required: true, message: '您的出生地是', trigger: 'blur' }],
  question2: [{ required: true, message: '您父亲的姓名是', trigger: 'blur' }],
  question3: [{ required: true, message: '您母亲的姓名是', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  confirmPassword: [{ required: true, message: '请确认新密码', trigger: 'blur' }],
});

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) {
    alert('表单不存在');
    return;
  }

  formEl.validate(async (valid) => {
    if (valid) {
      if (currentStep.value === 1) {
        // 向后端请求验证
        const response = await fetch('http://127.0.0.1:8000/api/find_password_confirm/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: ruleForm.userId,
            answer: `${ruleForm.question1},${ruleForm.question2},${ruleForm.question3}`,
          }),
        });

        const data = await response.json();

        if (data.success) {
          alert('验证成功');
          currentStep.value = 2;  // 切换到第二步
          stepperKey.value++;     // 强制刷新步骤器
        } else {
          alert(data.message);
        }
      } else if (currentStep.value === 2) {
        // 向后端请求更新密码
        const response = await fetch('http://127.0.0.1:8000/api/find_password_newpass/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: ruleForm.userId,
            password: ruleForm.newPassword,
            okPassword: ruleForm.confirmPassword,
          }),
        });

        const data = await response.json();

        if (data.success) {
          alert('密码更新成功');
        } else {
          alert(data.message);
        }
      }
    } else {
      alert('表单验证失败');
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();

  // 清空表单字段
  ruleForm.userId = '';
  ruleForm.question1 = '';
  ruleForm.question2 = '';
  ruleForm.question3 = '';
  ruleForm.newPassword = '';
  ruleForm.confirmPassword = '';

  // 重置为第一步
  currentStep.value = 1;
  stepperKey.value++;    // 更新 stepperKey 强制刷新
};
</script>

<style scoped>
/* 样式根据你的需求调整 */



.page-container {
  background-color: transparent; 
  display: flex;
  flex-direction: column;
  position: relative;
  justify-content: center;
  margin-top: 190px;
  width: 1000px;
}

.custom-stepper {
  width: 1100px;
  height: 940px;
  margin: 70px auto 0;
  padding: 20px;
}

.custom-card {
  width: 100%;
  height: 100%;
  max-width: 600px;
  margin: 100px auto;
}



.input-spacing {
  margin-bottom: 30px;
  /* 增加输入框之间的间距 */
}

.confirm-button {
  display: block;
  /* 确保按钮是块级元素，以便对齐 */
  margin: 20px auto;
  /* 设置外边距以确保按钮在卡片底部居中对齐 */
  height: 40px;
  /* 设置按钮高度以对齐 */
}

.image-container {
  position: relative;
}

.full-width-image {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
}

.button-container {
  display: flex;
  margin-top: 20px;
  justify-content: center;
  align-items: center;

}

.v-application {
  display: flex;
  background: rgba(255, 255, 255, 0);
  
}

.card {
  background-color: rgba(33, 60, 127, 0.401); /* 设置背景透明 */
  border-radius: 30px;
  padding: 20px;

  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  width: 100%;
}
.v-stepper.v-sheet {
  border-radius: 10px;
}
</style>