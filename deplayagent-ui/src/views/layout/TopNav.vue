<template>
  <div class="top-nav" v-show="isLogin">
    <!-- 左侧logo和标题 -->
    <div class="nav-left">
      <span class="nav-operation" @click="handleNavOperation"><el-icon class="nav-logo"><Operation /></el-icon></span>
      <span class="nav-title">云网盘</span>
    </div>

    <!-- 中间搜索框 -->
    <div class="nav-center">
      <el-input
          v-model="searchText"
          placeholder="搜索文件或文件夹..."
          prefix-icon="Search"
          class="search-input"
          @keyup.enter="handleSearch"
      ></el-input>
    </div>

    <!-- 右侧用户区域 -->
    <div class="nav-right">
      <!-- 通知图标 -->
      <el-button
          icon="Bell"
          circle
          type="text"
          class="nav-btn"
          @click="showNotification"
      ></el-button>

      <!-- 用户信息与下拉菜单 -->
      <div class="user-area" @click.stop="toggleUserMenu">
        <el-avatar class="user-avatar" :src="userAvatar">
          <span v-if="!userAvatar" class="avatar-placeholder">{{ userInitial }}</span>
        </el-avatar>
        <span class="user-name">{{ userName }}</span>

        <!-- 下拉菜单 -->
        <div
            class="user-dropdown"
            v-if="userMenuVisible"
            @click.stop
        >
          <div class="dropdown-item" @click="handleProfile">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </div>
          <div class="dropdown-item" @click="handleSettings">
            <el-icon><Setting /></el-icon>
            <span>账号设置</span>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item danger" @click="handleLogout">
            <el-icon><Logout /></el-icon>
            <span>退出登录</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, onUnmounted} from 'vue'
import { useRouter } from 'vue-router'
import {
  User, Setting, Logout, Operation
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import eventBus from '@/utils/eventBus'
import {userAPI} from "@/api/userinfo";

// 状态管理
const searchText = ref('')
const userMenuVisible = ref(false)
const userInfo = ref({
  name: '',
  avatar: '',
  username: ''
})
const isLogin = ref(localStorage.getItem('isLogin') === 'true')

// 路由实例
const router = useRouter()

// 计算属性：用户姓名首字母
const userInitial = computed(() => {
  return userInfo.value.name ? userInfo.value.name.charAt(0).toUpperCase() : 'U'
})

// 快捷访问用户信息
const userName = computed(() => userInfo.value.name || userInfo.value.username)
const userAvatar = computed(() => userInfo.value.avatar)

const handleNavOperation = () => {
    const miniNavValue = localStorage.getItem('miniNav')
    let value = false;
    if (miniNavValue) {
        localStorage.removeItem('miniNav')
    } else {
        value = true;
        localStorage.setItem('miniNav', "true")
    }
    eventBus.emit('data-event', {type: 'miniNav', value: value})
}

// 切换用户下拉菜单
const toggleUserMenu = () => {
  userMenuVisible.value = !userMenuVisible.value
}

// 点击其他区域关闭下拉菜单
const closeUserMenu = (e) => {
  if (!e.target.closest('.user-area')) {
    userMenuVisible.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  if (searchText.value.trim()) {
    ElMessage.success(`搜索: ${searchText.value}`)
    // 实际项目中可跳转到搜索结果页
    // router.push({ path: '/search', query: { q: searchText.value } })
  }
}

// 通知提示
const showNotification = () => {
  ElMessage.info('暂无新通知')
}

// 个人信息
const handleProfile = () => {
  userMenuVisible.value = false
  router.push('/profile') // 需创建个人信息页
}

// 账号设置
const handleSettings = () => {
  userMenuVisible.value = false
  router.push('/settings')
}

// 退出登录
const handleLogout = () => {
  userMenuVisible.value = false
  // 清除登录状态
  localStorage.clear();
  // 跳转到登录页
  router.push('/login')
  ElMessage.success('已退出登录')
}

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const res = await userAPI.info()
    userInfo.value = res
  } catch (error) {
    console.error('获取用户信息失败', error)
  }
}

const handleReceivedData = (data) => {
    if (data && data['type']) {
        const type = data['type']
        const value = data['value']
        if (type === 'isLogin') {
            isLogin.value = value
        }
    }
}

// 初始化
onMounted(() => {
  // 获取用户信息
  if (isLogin.value) {
    fetchUserInfo()
  }
  eventBus.on('data-event', handleReceivedData)
  // 监听点击事件关闭下拉菜单
  document.addEventListener('click', closeUserMenu)
})

// 清理事件监听
onUnmounted(() => {
  document.removeEventListener('click', closeUserMenu)
  eventBus.off('data-event', handleReceivedData)
})
</script>

<style scoped>
.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 10;
}

/* 左侧logo区域 */
.nav-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-operation {
    cursor: pointer;
}
.nav-logo {
  color: #409eff;
  font-size: 24px;
}

.nav-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 中间搜索区域 */
.nav-center {
  flex: 1;
  max-width: 600px;
  margin: 0 20px;
}

.search-input {
  width: 100%;
  background-color: #f5f7fa;
  border: none;
  transition: all 0.3s;
}

.search-input:focus {
  background-color: #fff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 右侧用户区域 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-btn {
  color: #606266;
  font-size: 18px;
  transition: color 0.3s;
}

.nav-btn:hover {
  color: #409eff;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.user-area:hover {
  background-color: #f5f7fa;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border: 2px solid #f0f2f5;
}

.avatar-placeholder {
  font-size: 16px;
  font-weight: bold;
}

.user-name {
  font-size: 14px;
  color: #303133;
  white-space: nowrap;
}

.user-arrow {
  font-size: 14px;
  color: #909399;
  transition: transform 0.3s;
}

.rotate {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.user-dropdown {
  position: absolute;
  top: 65px;
  right: 20px;
  width: 180px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  padding: 5px 0;
  z-index: 100;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  font-size: 14px;
  color: #303133;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f5f7fa;
}

.dropdown-item.el-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.dropdown-item.danger {
  color: #ff4d4f;
}

.dropdown-item.danger:hover {
  background-color: #fff5f5;
}

.dropdown-divider {
  height: 1px;
  margin: 5px 0;
  background-color: #f0f0f0;
}
</style>
