<template>
  <div class="image-container">
    <img src='/Logos/RegisterTitle.png' alt="title" class="full-width-image" />
  </div>
  <div class='page-container'>
    <v-app>
      <v-container>
        <div class="card">
          <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" status-icon :rules="rules"
            label-width="auto" class="demo-ruleForm">

            <el-form-item label="用户ID" prop="id" :error="idError">
              <p>请输入您想创建的用户id</p>
              <el-input v-model="ruleForm.id" type="id" autocomplete="off" />
            </el-form-item>

            <el-form-item label="密码" prop="pass" :error="passwordError">
              <p>请输入您的密码(8-20位数字或字母)</p>
              <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
            </el-form-item>

            <el-form-item label="确认密码" prop="checkPass">
              <p>请再次确认您的密码</p>
              <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
            </el-form-item>

            <el-form-item label="保密问题1" prop="q1">
              <p>您的出生地是？</p>
              <el-input v-model="ruleForm.q1" />
            </el-form-item>

            <el-form-item label="保密问题2" prop="q2">
              <p>您父亲的姓名是？</p>
              <el-input v-model="ruleForm.q2" />
            </el-form-item>

            <el-form-item label="保密问题3" prop="q3">
              <p>您母亲的姓名是？</p>
              <el-input v-model="ruleForm.q3" />
            </el-form-item>

            <el-form-item style="margin-left: 180px;margin-top: 30px">
              <el-button type="primary" @click="submitForm(ruleFormRef)">
                提交
              </el-button>
              <el-button @click="resetForm(ruleFormRef)">重置</el-button>
            </el-form-item>
          </el-form>

          <div class='button-container'>
            <WhiteButton width='150px' height='40px' style='margin-left: 0px' @click="router.push('/welcome')">
              <p style='font-size: 15px'>返回welcome界面</p>
            </WhiteButton>
          </div>
        </div>
      </v-container>
    </v-app>
  </div>
</template>

<script setup lang='ts'>
import { useRouter } from 'vue-router'
const router = useRouter()
import { reactive, ref } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';

const ruleFormRef = ref<FormInstance>();
const idError = ref('');
const passwordError = ref('');

const checkid = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入用户id'));
  }
  setTimeout(() => {
    // 确保值是字符串类型并且长度为8
    if (typeof value !== 'string' || value.length !== 8) {
      return callback(new Error('请输入8位纯数字'));
    }
    // 确保所有字符都是数字
    if (!/^\d+$/.test(value)) {
      return callback(new Error('请输入纯数字'));
    }
    callback(); // 通过验证
  }, 1);
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return;
      ruleFormRef.value.validateField('checkPass');
    }
    callback();
  }
}

const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== ruleForm.pass) {
    callback(new Error("两次输入的密码不一致！"));
  } else {
    callback();
  }
}

const validateQuestion = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('此项不能为空'));
  } else {
    callback();
  }
}

const ruleForm = reactive({
  id: '',
  pass: '',
  checkPass: '',
  q1: '',
  q2: '',
  q3: ''
});

const rules = reactive<FormRules<typeof ruleForm>>({
  id: [{ validator: checkid, trigger: 'blur' }],
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  q1: [{ validator: validateQuestion, trigger: 'blur' }],
  q2: [{ validator: validateQuestion, trigger: 'blur' }],
  q3: [{ validator: validateQuestion, trigger: 'blur' }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      // 清除之前的错误信息
      idError.value = '';
      passwordError.value = '';

      // const url = 'http://localhost:3000/register';
      const url = 'http://127.0.0.1:8000/api/register/';
      console.log('Sending request to:', url); // 打印请求URL

      // 发送请求到后端进行注册
      fetch(url, {
        method: 'POST', // 确保使用POST请求
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: ruleForm.id,
          password: ruleForm.pass,
          okPassword: ruleForm.checkPass,
          answer: ruleForm.q1 + ',' + ruleForm.q2 + ',' + ruleForm.q3, // 将三个问题的答案合并为一个字符串
        }),
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(data.message);
            });
          }
          return response.json();
        })
        .then(data => {
          if (data.success) {
            console.log('Registration successful:', data.message);
            alert('Registration successful')
            router.push('/login/user')

            // 处理注册成功后的逻辑
          } else {
            console.error('Registration failed:', data.message);
            // 处理注册失败后的逻辑
          }
        })
        .catch(error => {
          console.error('Error registering:', error);
          // 处理注册错误后的逻辑
          if (error.message.includes('ID已存在')) {
            idError.value = error.message;
          } else if (error.message.includes('密码不符合要求')) {
            passwordError.value = error.message;
          } else {
            alert(error.message);
          }
        });
    } else {
      console.log('error submit!');
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
  idError.value = '';
  passwordError.value = '';
};
</script>

<style scoped>
.page-container {
  background-color: transparent; 
  display: flex;
  flex-direction: column;
  margin-top: 170px;
   /*min-height: 100vh; 确保页面背景色覆盖整个视口 */
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

.card {
  background-color: rgba(255, 255, 255, 0.661); /* 设置背景透明 */
  border-radius: 30px;
  padding: 20px;
  margin: 20px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  max-width: 600px;
  width: 100%;
}

.v-application {
  display: flex;
  background: rgba(255, 255, 255, 0);
  
}

.v-application__wrap {
  backface-visibility: hidden;
  display: flex
;
  flex-direction: column;
  flex: 1 1 auto;
  max-width: 100%;
  /* min-height: 100vh; */
  /* min-height: 100dvh; */
  position: relative;
}

/* 使用 ::v-deep 选择器覆盖 Element Plus 组件的样式 */
::v-deep .el-form-item__label,
::v-deep .el-form-item__content p {
  color: black; /* 设置文字颜色为白色 */
}
</style>