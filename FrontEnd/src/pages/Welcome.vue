<template>
  <div class="page-container">
    
    <div class="content-container">
      <div style="margin-bottom: 60px; justify-content: center; align-items: center; display: flex;">
        <img src="/Logos/Icon.png" style="width: 150px; border-radius: 30px;" alt="Icon">
        <img src="/Logos/Logo.png" style="width: 600px;" alt="Logo">
      </div>

      <div class="drop-down">
        <p style="font-size: 24px; margin-right: 40px">请选择登录角色</p>
        <el-select v-model="value" placeholder="身份" size="large" style="width: 100px">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>

      <div class="button-container">
        <ShadowButton width="221px" height="60px" style="margin-left: 50px" @click="login">
          <p style="font-size: 24px; margin-right: 10px">登录</p>
        </ShadowButton>
        <ShadowButton width="221px" height="60px" style="margin-left: 50px" @click="handleRegister">
          <p style="font-size: 24px; margin-right: 10px">注册</p>
        </ShadowButton>
      </div>

      <el-dialog :model-value="dialogVisible" title="提示" @close="dialogVisible = false">
        <span>管理员账号不能注册</span>
      </el-dialog>


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

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ShadowButton from "@/components/ShadowButton.vue";

const router = useRouter();

// 第一个模板的逻辑
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

// 第二个模板的逻辑
const dialogVisible = ref(false);
const value = ref("");

const options = [
  {
    value: "user",
    label: "用户",
  },
  {
    value: "manager",
    label: "管理员",
  },
];

const login = () => {
  if (value.value === "user") {
    router.push("/login/user");
  } else if (value.value === "manager") {
    router.push("/login/manager");
  } else {
    alert("请选择登录角色");
  }
};

const handleRegister = () => {
  if (value.value === "user") {
    router.push("/register");
  } else if (value.value === "manager") {
    dialogVisible.value = true;
  } else {
    router.push("/register");
  }
};
</script>

<style lang="scss" scoped>
.page-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  
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

.drop-down {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.button-container {
  display: flex;
  margin-top: 60px;
  justify-content: center;
  align-items: center;
}

.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>