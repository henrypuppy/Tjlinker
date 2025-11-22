<template>
  <div class="container">
    <aside class="aside">
      <!-- 此处可放置侧边栏内容 -->
      <el-tag size="large">个人资料编辑</el-tag>
      <div class="aside-avatar">
        <img :src="avatarUrl" alt="User Avatar"
          style="width: 130px; height: 130px; margin-top: 7px; border-radius: 50%; object-fit: cover" />
      </div>
    </aside>
    <main class="main">
      <div class="profile-container">
        <div class="profile-content">
          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              头像：
            </el-col>
            <el-col :span="16">
              <el-upload action="#" list-type="picture-card" v-model:file-list="fileList" :on-change="handleFileChange"
                :auto-upload="false" :limit="1" :disabled="isUploadDisabled" :on-remove="handleRemove" ref="uploadRef">
                <el-icon>
                  <Plus />
                </el-icon>

                <template #file="{ file }">
                  <div>
                    <img class="el-upload-list__item-thumbnail" :src="file.url" alt=""
                      style="max-width: 70px; max-height: 70px; object-fit: contain;" />
                    <span class="el-upload-list__item-actions">
                      <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                        <el-icon>
                          <ZoomIn />
                        </el-icon>
                      </span>
                      <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove">
                        <el-icon>
                          <Delete />
                        </el-icon>
                      </span>
                    </span>
                  </div>
                </template>
              </el-upload>

              <el-dialog v-model="dialogVisible" title="头像预览">
                <!-- 设置图片的样式来限制宽高为 200x200 -->
                <img :src="dialogImageUrl" alt="Preview Image"
                  style="width: 400px; height: 400px; object-fit: cover;" />
              </el-dialog>
            </el-col>
          </el-row>

          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              ID:
            </el-col>
            <el-col :span="2">
              <el-tag type="info">{{ id }}</el-tag>
            </el-col>
          </el-row>

          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              昵称:
            </el-col>
            <el-col :span="13" style="display: flex; align-items: center;">
              <el-input v-model="input" style="width: 240px; margin-right: 10px;" placeholder="请输入昵称"
                @blur="validateNickname" @input="checkNicknameLength" />
              <span v-if="nicknameError" style="color: red; font-size: 12px;">{{ nicknameError }}</span>
            </el-col>
          </el-row>


          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              性别：
            </el-col>
            <el-col :span="3">
              <el-select v-model="gender" placeholder="请选择性别">
                <el-option label="男" value="男"></el-option>
                <el-option label="女" value="女"></el-option>
              </el-select>
            </el-col>
          </el-row>

          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              个人简介：
            </el-col>
            <el-col :span="5">
              <el-input v-model="textarea" style="width: 500px" :autosize="{ minRows: 4, maxRows: 4 }" type="textarea"
                placeholder="这个人好懒什么都没有写~" />
            </el-col>
          </el-row>

          <el-row type="flex" align="middle" class="profile-row">
            <el-col :span="5">
              兴趣标签：
            </el-col>
            <el-col :span="10">
              <div class="flex gap-2">
                <el-tag v-for="tag in dynamicTags" :key="tag" closable :disable-transitions="false"
                  @close="handleClose(tag)">
                  {{ tag }}
                </el-tag>
                <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="w-20" size="small"
                  @keyup.enter="handleInputConfirm" @blur="handleInputConfirm" />
                <el-button v-else class="button-new-tag" size="small" @click="showInput"
                  :disabled="dynamicTags.length >= 3">
                  + New Tag
                </el-button>
              </div>
              <p style="margin-top: 5px; font-size: 12px; color: #999;">
                当前已添加 {{ dynamicTags.length }}/3 个标签
              </p>
            </el-col>
          </el-row>

          <!-- 确定和返回按钮 -->
          <el-row type="flex" justify="end" class="profile-row">
            <el-button type="primary" @click="submitProfile">确定</el-button>
            <el-button class="ml-2" @click="handleBack">返回</el-button>
          </el-row>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Delete, Plus, ZoomIn } from '@element-plus/icons-vue'
import { nextTick } from 'vue'
import type { InputInstance } from 'element-plus'
import type { UploadFile, UploadInstance } from 'element-plus'
import { useRouter } from 'vue-router'

const fileList = ref<UploadFile[]>([]) // 只有一张图片
const isUploadDisabled = ref(false) // 控制上传按钮是否禁用

const gender = ref(localStorage.getItem('userGender') || '')
const input = ref(localStorage.getItem('userName') || '')
const textarea = ref(localStorage.getItem('userBio') || '')
const avatarUrl = ref(localStorage.getItem('userAvatar') || '')

const inputValue = ref('') // 兴趣标签
const inputVisible = ref(false) // 兴趣标签
const InputRef = ref<InputInstance>() // 兴趣标签
// const dynamicTags = ref(localStorage.getItem('userTags')?.split(',') || []) // 保证 dynamicTags 是 ref
const dynamicTags = ref( // 过滤掉可能的空值
  (localStorage.getItem('userTags')?.split(',') || []).filter(tag => tag.trim() !== '')
)

const id = localStorage.getItem('userId')

const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const disabled = ref(false)

const handleRemove = () => {
  fileList.value = [] // 移除图片
  isUploadDisabled.value = false // 重新启用上传按钮
}

const handlePictureCardPreview = (file: UploadFile) => {
  dialogImageUrl.value = file.url!
  dialogVisible.value = true
}

// Tags
const handleClose = (tag: string) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value!.input!.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value.length > 4) {
    alert('标签字数不能超过 4 个字符！')
    inputVisible.value = false
    inputValue.value = ''
    return
  }
  if (inputValue.value.length < 1) {
    alert('标签不能为空！')
    inputVisible.value = false
    inputValue.value = ''
    return
  }
  if (inputValue.value) {
    dynamicTags.value.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

// 检查文件格式和大小
const uploadRef = ref<UploadInstance>()
const handleFileChange = (file: UploadFile, fileList: UploadFile[]) => {
  console.log('File added:', file)
  console.log('Current file list:', fileList)

  // 检查文件类型是否为 PNG 或 JPG
  const isPNGorJPG = file.raw?.type === 'image/png' || file.raw?.type === 'image/jpeg'
  if (!isPNGorJPG) {
    alert('仅支持上传 PNG 或 JPG 格式的图片文件！')
    fileList = [] // 清空文件列表
    isUploadDisabled.value = false // 重新启用上传按钮
    return
  }

  // 检查文件大小是否超过 2MB
  const maxSizeInMB = 2
  if ((file.raw?.size || 0) / 1024 / 1024 > maxSizeInMB) {
    alert('文件大小不能超过 2MB！')
    fileList = [] // 清空文件列表
    isUploadDisabled.value = false // 重新启用上传按钮
    return
  }

  if (fileList.length >= 1) {
    isUploadDisabled.value = true // 已上传一张图片，禁用上传按钮
  }

  // 设置头像的 URL（上传完成后）
  avatarUrl.value = file.url!
}

const router = useRouter()
const handleBack = () => {
  router.push('/person')
}

const nicknameError = ref(''); // 错误提示

const validateNickname = () => {
  if (!input.value.trim()) {
    nicknameError.value = '昵称不能为空！';
  } else {
    nicknameError.value = '';
  }
};

const checkNicknameLength = () => {
  if (input.value.length > 10) {
    input.value = input.value.slice(0, 10); // 限制字符长度
    nicknameError.value = '昵称不能超过10个字符！';
  } else {
    nicknameError.value = '';
  }
};

// POST
const submitProfile = async () => {
  if (!input.value.trim()) {
    return; // 阻止提交
  }

  const sexBool = gender.value === '男' ? true : false;
  const introText = textarea.value.trim() === '' ? '这个人好懒还什么都没有写~' : textarea.value;

  // 创建 FormData 对象
  const formData = new FormData();
  formData.append('id', id!);
  formData.append('name', input.value);
  formData.append('sex', sexBool.toString());
  formData.append('intro', introText);
  formData.append('tags', dynamicTags.value.join(','));

  // 如果头像文件存在，添加到 formData 中
  if (fileList.value.length > 0) {
    formData.append('image', fileList.value[0].raw as Blob);
  }

  // 使用 forEach 打印 FormData
  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });

  const url = `http://127.0.0.1:8000/api/users/edit_info/`;

  try {
    // 发起 POST 请求，使用 FormData 传输文件
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        // 如果需要身份验证，可以在这里添加 Authorization 头部
        // 'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
      },
      body: formData, // 使用 FormData 作为请求体
    });

    if (response.ok) {
      const result = await response.json();
      alert('个人资料更新成功！');
      console.log('后端返回的数据：', result);
      router.push('/person');
    } else {
      const error = await response.json();
      console.error('更新失败：', error);
      alert('更新失败，请稍后重试。');
    }
  } catch (error) {
    console.error('提交个人资料时发生错误：', error);
    alert('网络错误，请检查网络连接或联系管理员。');
  }
};

</script>

<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.el-upload-list--picture-card .el-upload-list__item {
  background-color: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color);
  border-radius: 6px;
  box-sizing: border-box;
  display: inline-flex;
  height: 70px;
  margin: 0 8px 8px 0;
  overflow: hidden;
  padding: 0;
  width: 70px;
}

.container {
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  background-color: #ffffff96;
  display: flex;
  height: 100vh;
}

.aside {
  width: 250px;
  background-color: #f3f4f6;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 让aside中的内容居中 */
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  padding: 20px;
}

.profile-container {
  width: 100%;
  max-width: 800px;
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  height: 750px;
}

.profile-row {
  margin-bottom: 20px;
}

.aside-avatar {
  margin-top: 20px;
  /* 上方增加一点间距 */
  display: flex;
  justify-content: center;
}

.avatar-image {
  margin-top: 45px;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-content {
  margin-top: 150px;
}

.el-upload--picture-card {
  --el-upload-picture-card-size: 50px;
}

.el-upload--picture-card {
  --el-upload-picture-card-size: 70px;
}
</style>
