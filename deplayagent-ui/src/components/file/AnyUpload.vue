<template>
    <el-upload
            class="any-upload"
            action="#"
            :http-request="handleUpload"
            :on-success="handleSuccess"
            :on-error="handleError"
            :file-list="fileList"
            :auto-upload="true"
            >
    <el-button type="primary">点击上传</el-button>
    <template #tip>
        <div class="el-upload__tip">
            只能上传 支持单文件上传，格式不限
        </div>
    </template>
  </el-upload>
</template>

<script setup>
import {defineEmits, ref} from 'vue';
import { anyUploadAPI } from '@/api/anyupload'

const fileList = ref([]);

const emit = defineEmits(['success', 'error'])

// 自定义上传方法
const handleUpload = async (params) => {
    const { file } = params;
    try {
        const response = await anyUploadAPI.upload(file, (progressEvent) => {
            // console.log("progressEvent", progressEvent)
            const percent = Math.round((progressEvent.loaded / progressEvent.total) * 100);
            console.log(`上传进度: ${percent}%`);
        });
        // 调用内置的成功回调（需要按el-upload的要求格式返回）
        emit('success', response, file);
        params.onSuccess(response);
    } catch (error) {
        // 调用内置的失败回调
        emit('error', error, file)
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
