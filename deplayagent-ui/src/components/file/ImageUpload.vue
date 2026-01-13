<template>
    <el-upload
        class="avatar-uploader"
        action="#"
        :http-request="handleUpload"
        :on-success="handleSuccess"
        :on-error="handleError"
        :auto-upload="true"
        >
      <el-avatar v-if="imageUrl" shape="square" :size="200" fit="fit" :src="imageUrl" />
      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
  </el-upload>
</template>

<script setup>
import { defineEmits,ref} from 'vue';
import { Plus } from '@element-plus/icons-vue'
import {eventBus} from "@/utils/eventBus";
import {downloads} from "@/utils/downloads";
import {ElMessage} from "element-plus";
import {anyUploadAPI} from "@/api/anyupload";
// import { UploadFile } from 'element-plus'

const imageUrl = ref('')

const emit = defineEmits(['success'])

eventBus.on('event:disk:add-avatar-url', async event=>{
  if (event) {
    await loadImgUrl(event)
  }
})

const loadImgUrl = async (path) => {
  try {
    const downUrl = await downloads.getDownTokeUrl(path)
    imageUrl.value = downUrl;
  } catch (err) {
    ElMessage.error("加载图片错误")
  }
}

const handleUpload = async (params) => {
    const { file } = params;
    try {
        const response = await anyUploadAPI.upload(file, (progressEvent) => {
            // console.log("progressEvent", progressEvent)
            const percent = Math.round((progressEvent.loaded / progressEvent.total) * 100);
            console.log(`上传进度: ${percent}%`);
        });
        // 调用内置的成功回调（需要按el-upload的要求格式返回）
        params.onSuccess(response);
        emit('success', {'refId': response['refId']})
        await loadImgUrl(response['path']);
    } catch (error) {
        // 调用内置的失败回调
        params.onError(error);
    }
};

// 上传成功处理
const handleSuccess = (response, file, fileList) => {
    console.log('上传成功', response, file, fileList);
    // 可以在这里处理后端返回的结果
};

// 上传失败处理
const handleError = (error, file, fileList) => {
    console.error('上传失败', error, file, fileList);
    // 可以在这里处理错误信息
};
</script>

<style>
.el-upload {
  border: 1px dashed #8d8d8d;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
.el-upload-list {
  display: none !important;
}
</style>
