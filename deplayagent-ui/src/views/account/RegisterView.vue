<template>
    <div class="login-page">
        <!-- 背景渐变装饰 -->
        <div class="bg-decoration top-left"></div>
        <div class="bg-decoration bottom-right"></div>

        <!-- 登录卡片 -->
        <div class="login-card">
            <!-- Logo 区域 -->
            <div class="login-header">
                <div class="login-logo">
                    <el-icon class="logo-icon">
                        <UserFilled />
                    </el-icon>
                </div>
                <h2 class="login-title">欢迎使用</h2>
                <p class="login-desc">请注册您的账号继续使用</p>
            </div>

            <!-- 登录表单 -->
            <el-form
                :model="loginForm"
                :rules="loginRules"
                ref="loginFormRef"
                label-width="0px"
                class="login-form"
            >
                <!-- 用户名输入框 -->
                <el-form-item prop="username" class="form-item">
                    <el-input
                        v-model="loginForm.username"
                        placeholder="请输入用户名"
                        class="custom-input"
                        :prefix="User"
                        :focus="isUsernameFocused"
                        @focus="isUsernameFocused = true"
                        @blur="isUsernameFocused = false"
                    />
                </el-form-item>
                <el-form-item prop="password" class="form-item">
                    <el-input
                        v-model="loginForm.password"
                        placeholder="请输入密码"
                        type="password"
                        class="custom-input"
                        :prefix="User"
                        :focus="isPhoneFocused"
                        @focus="isPhoneFocused = true"
                        @blur="isPhoneFocused = false"
                        @keydown.enter="handleLogin"
                    />
                </el-form-item>
                <el-form-item prop="password1" class="form-item">
                  <el-input
                      v-model="loginForm.password1"
                      placeholder="请再次输入密码"
                      type="password"
                      class="custom-input"
                      :prefix="User"
                      :focus="isPasswordFocused"
                      @focus="isPasswordFocused = true"
                      @blur="isPasswordFocused = false"
                      @keydown.enter="handleLogin"
                  />
                </el-form-item>

                <el-form-item prop="nickName" class="form-item">
                  <el-input
                      v-model="loginForm.nickName"
                      placeholder="请输入昵称"
                      class="custom-input"
                      :prefix="User"
                      :focus="isNickNameFocused"
                      @focus="isNickNameFocused = true"
                      @blur="isNickNameFocused = false"
                  />
                </el-form-item>

                <el-form-item prop="email" class="form-item">
                  <el-input
                      v-model="loginForm.email"
                      placeholder="请输入邮箱"
                      class="custom-input"
                      :prefix="User"
                      :focus="isEmailFocused"
                      @focus="isEmailFocused = true"
                      @blur="isEmailFocused = false"
                  />
                </el-form-item>

                <!-- 登录按钮 -->
                <el-form-item class="form-item">
                    <el-button
                        type="primary"
                        @click="handleLogin"
                        class="login-btn flex-full"
                        block
                        :loading="isLoading"
                    >
                        <span v-if="!isLoading">注册</span>
                        <span v-else>注册中...</span>
                    </el-button>
                </el-form-item>

                <!-- 辅助链接 -->
                <div class="login-links">
                    <router-link to="/login" class="link-item">已有账号</router-link>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { UserFilled, User } from '@element-plus/icons-vue'
import { ElMessage, ElForm, ElFormItem, ElInput, ElButton } from 'element-plus'
import {authAPI} from "@/api/login";

const loginFormRef = ref(null)
const isLoading = ref(false) // 登录加载状态
const isUsernameFocused = ref(false) // 用户名输入框聚焦状态
const isPhoneFocused = ref(false) // 手机号输入框聚焦状态
const isPasswordFocused = ref(false) // 手机号输入框聚焦状态
const isNickNameFocused = ref(false) // 手机号输入框聚焦状态
const isEmailFocused = ref(false) // 手机号输入框聚焦状态

// 登录表单数据
const loginForm = reactive({
    username: '',
    nickName: '',
    password: '',
    email: null,
    password1: '',
})

// 表单验证规则
const loginRules = reactive({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '用户名长度为6-20个字符', trigger: 'blur' }
    ],
    password1: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 20, message: '用户名长度为6-20个字符', trigger: 'blur' }
    ],
    nickName: [
      { required: true, message: '请输入昵称', trigger: 'blur' },
      { min: 6, max: 20, message: '昵称长度为6-20个字符', trigger: 'blur' }
    ]
})

// 登录处理
const handleLogin = async () => {
    try {
        // 表单验证
        await loginFormRef.value.validate()

        if (loginForm.password !== loginForm.password1) {
          ElMessage.info('两次密码不匹配')
          return
        }
        // 模拟登录加载
        isLoading.value = true
        await authAPI.register({
            userName: loginForm.username,
            nickName: loginForm.nickName,
            password: loginForm.password,
            email: loginForm.email,
            ac: "ac"
        });
        isLoading.value = false
        ElMessage.success('注册成功')
    } catch (error) {
        // ElMessage.error('注册失败，请检查输入')
        console.error('注册表单验证失败:', error)
    }
}
</script>

<style scoped lang="scss">
@import "@/assets/css/account.scss";
/* 固定容器高度 100% */
.login-page {
    width: 100%;
    height: 100vh;
    position: relative;
    background-color: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.25rem 0.15rem; /* 25px 15px */
    overflow: hidden;
}

/* 背景装饰（Rem 尺寸） */
.bg-decoration {
    position: absolute;
    width: 3rem; /* 300px */
    height: 3rem;
    border-radius: 50%;
    opacity: 0.15;
    z-index: 0;
}

.top-left {
    top: -1rem; /* -100px */
    left: -1rem;
    background: linear-gradient(135deg, #409eff, #69b1ff);
}

.bottom-right {
    bottom: -1rem;
    right: -1rem;
    background: linear-gradient(135deg, #722ed1, #9370db);
}

/* 登录卡片（Rem 尺寸） */
.login-card {
    width: 100%;
    max-width: 3.45rem; /* 345px */
    background-color: #fff;
    border-radius: 0.2rem; /* 20px */
    box-shadow: 0 0.1rem 0.3rem rgba(0, 0, 0, 0.08);
    padding: 0.4rem 0.3rem; /* 40px 30px */
    position: relative;
    z-index: 1;
    transform: translateY(0);
    transition: all 0.3s ease;
}

.login-card:hover {
    box-shadow: 0 0.15rem 0.35rem rgba(0, 0, 0, 0.12);
    transform: translateY(-0.05rem); /* -5px */
}

/* 登录头部 */
.login-header {
    text-align: center;
    margin-bottom: 0.4rem; /* 40px */
}

.login-logo {
    width: 0.8rem; /* 80px */
    height: 0.8rem;
    background: linear-gradient(135deg, #409eff, #722ed1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.2rem; /* 20px */
    box-shadow: 0 0.04rem 0.15rem rgba(64, 158, 255, 0.3);
}

.logo-icon {
    font-size: 0.4rem !important; /* 40px */
    color: #fff;
}

.login-title {
    font-size: 0.24rem; /* 24px */
    font-weight: 600;
    color: #1d2129;
    margin-bottom: 0.08rem; /* 8px */
}

.login-desc {
    font-size: 0.14rem; /* 14px */
    color: #86909c;
}

/* 表单样式 */
.login-form {
    width: 100%;
}

.form-item {
    margin-bottom: 0.2rem; /* 20px */
}

.custom-input {
    border-radius: 0.225rem !important; /* 22.5px */
    height: 0.45rem !important; /* 45px */
    font-size: 0.16rem !important; /* 16px */
    border: 0.01rem solid #e5e6eb !important; /* 1px */
    transition: all 0.3s ease;
}

.custom-input:focus-within {
    border-color: #409eff !important;
    box-shadow: 0 0 0 0.02rem rgba(64, 158, 255, 0.15) !important; /* 2px */
}

.el-input__prefix {
    color: #86909c !important;
    font-size: 0.2rem !important; /* 20px */
    margin-right: 0.1rem !important; /* 10px */
}

.custom-input:focus-within .el-input__prefix {
    color: #409eff !important;
}

/* 登录按钮 */
.login-btn {
    background: linear-gradient(135deg, #409eff, #69b1ff) !important;
    border: none !important;
    height: 0.5rem !important; /* 50px */
    font-size: 0.17rem !important; /* 17px */
    font-weight: 500 !important;
    border-radius: 0.25rem !important; /* 25px */
    transition: all 0.3s ease;
    box-shadow: 0 0.04rem 0.12rem rgba(64, 158, 255, 0.2);
}

.login-btn:hover {
    background: linear-gradient(135deg, #3689e6, #5ba0ff) !important;
    box-shadow: 0 0.06rem 0.16rem rgba(64, 158, 255, 0.25);
}

.login-btn:active {
    transform: scale(0.98);
}

/* 辅助链接 */
.login-links {
    display: flex;
    justify-content: space-between;
    margin-top: 0.15rem; /* 15px */
    margin-bottom: 0.4rem; /* 40px */
}

.link-item {
    font-size: 0.14rem; /* 14px */
    color: #409eff;
    text-decoration: none;
    transition: color 0.3s ease;
}

.link-item:hover {
    color: #3689e6;
    text-decoration: underline;
}

/* 游客登录 */
.guest-login {
    text-align: center;
    margin-top: 0.25rem; /* 25px */
}

.guest-link {
    display: inline-flex;
    align-items: center;
    font-size: 0.15rem; /* 15px */
    color: #86909c;
    text-decoration: none;
    transition: all 0.3s ease;
}

.guest-link:hover {
    color: #409eff;
}

.guest-icon {
    font-size: 0.16rem !important; /* 16px */
    margin-left: 0.05rem; /* 5px */
    transition: transform 0.3s ease;
}

.guest-link:hover .guest-icon {
    transform: translateX(0.02rem); /* 2px */
}
</style>
