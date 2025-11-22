<template>
  <div class="page-container" >

    <div class="content-container">
    <div style="margin-bottom: 60px; justify-content: center; align-items: center; display: flex;">
      <ImageButton
        url="/some-page"
        imageSrc="/Logos/Icon.png"
        altText="Example Image"
        width="150px"
        height="176.9px"
        @click="router.push('/welcome')"
      />
      <img src='/Logos/Logo.png' style='width: 600px;' alt='Logo'>
    </div>

    <div class='input-container'>
      <el-icon :size="40">
        <User />
      </el-icon>
      <el-input v-model="input_id" style="width: 300px; height: 60px; margin-left: 20px;" placeholder="请输入" />
    </div>

    <div class='input-container'>
      <el-icon :size="40">
        <Lock />
      </el-icon>
      <el-input v-model="input_password" style="width: 300px; height: 60px; margin-left: 20px;" placeholder="请输入" type="password" show-password />
    </div>
    
    <div class='button-container'>
      <ShadowButton width='221px' height='60px' style='margin-left: 50px' @click="handleLogin">
        <p style='font-size: 24px; margin-right: 10px'>登录</p>
      </ShadowButton>

      <WhiteButton width='100px' height='40px' style='margin-left: 50px' @click="router.push('/find-password')">
        <p style='font-size: 15px; margin-right: 10px'>忘记密码</p>
      </WhiteButton>
    </div> 


    <div ref="container" class="box" @click="handleRandom">
        <span
          :key="childKey"
          ref="child"
          :style="{ color: colorRandom(), left: childLeft, top: childTop }"
          class="minbox"
        >
          {{ msg }}
        </span>
      </div>
  </div>
</div>
</template>

<script setup >
import { Lock, User } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const input_id = ref('')
const input_password = ref('')
const router = useRouter()

const handleLogin = async () => {
  if (!input_id.value) {
    alert('Please enter ID')
    return
  }
  if (!input_password.value) {
    alert('Please enter password')
    return
  }

  const url = 'http://127.0.0.1:8000/api/userlogin/'
  console.log('Sending request to:', url) // 打印请求URL

  // 发送请求到后端进行登录
  fetch(url, {
    method: 'POST', // 确保使用POST请求
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: input_id.value,
      password: input_password.value,
    }),
  })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.message)
        })
      }
      return response.json()
    })
    .then(data => {
      if (data.success) {
        alert('login succeed')
        localStorage.clear();
        localStorage.setItem('userId', input_id.value);
        localStorage.setItem('isAdmin', 'no');
      
        router.push('/home')
      } else {
        alert(data.message)
      }
    })
    .catch(error => {
      console.error('Error logging in:', error)
      alert(error.message)
    })
}

// 点击特效逻辑
const container = ref(null);
const child = ref(null);
const childKey = ref(0);

const colorRandom = () => {
  let color;
  do {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    color = `rgb(${r},${g},${b})`;
  } while (color === "rgb(250,235,215)");
  return color;
};

const textArr = [
  "😒",
  "💕😁😊😂🤣❤️😍👌😘🙌👍😎😉🎶💖😜😀😁😃😄😅😆😂🤣😉😊😋😎😍😘🥰😗😙🥲😚☺️🙂🤗🤩🤔🫡🤨😯🤐🫠🤡🥳🥺🥹🧐🧐👻🤖🤖",
  "💕",
  "😁",
  "😊",
  "😂",
  "🤣",
  "❤️",
  "😍",
  "👌",
  "😘",
  "🙌",
  "👍",
  "😎",
  "😉",
  "🎶",
  "💖",
  "😜",
  "😀",
  "😁",
  "😃",
  "😄",
  "😅",
  "😆",
  "😂",
  "🤣",
  "😉",
  "😊",
  "😋",
  "😎",
  "😍",
  "😘",
  "🥰",
  "😗",
  "😙",
  "🥲",
  "😚",
  "🙂",
  "🤗",
  "🤩",
  "🤔",
  "🫡",
  "🤨",
  "😯",
  "🤐",
  "🫠",
  "🤡",
  "🥳",
  "🥺",
  "🥹",
  "🧐",
  "👻",
  "🤖",
];

const randomInd = () => {
  return Math.floor(Math.random() * textArr.length);
};

const msg = ref(null);
const childLeft = ref(0);
const childTop = ref(0);

const handleRandom = (e) => {
  childLeft.value = e.clientX + "px";
  childTop.value = e.clientY + "px";
  msg.value = textArr[randomInd()];
  childKey.value++;
};
</script>

<style lang="scss" scoped>
.page-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.input-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
}

.button-container {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
  justify-content: center;
  align-items: center;
}

.box {
  position: absolute;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  cursor: pointer;
  background-color: rgb(255, 255, 255);
  overflow: hidden;
  z-index: -1; /* 确保背景板在内容下面 */

  .minbox {
    width: fit-content;
    position: absolute;
    animation: moveAndFadeout 1s ease-in-out forwards;
  }

  @keyframes moveAndFadeout {
    0% {
      transform: translate(0, 0) scale(1) rotate(0deg);
      opacity: 1;
    }
    100% {
      transform: translate(20px, -80px) rotate(180deg) scale(2);
      opacity: 0;
    }
  }
}

.content-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1; /* 确保内容在背景板上面 */
}

</style>