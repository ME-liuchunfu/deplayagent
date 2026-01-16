<template>
    <div class="aside-menu" :class="{'mini-menu': miniNav}" v-if="isLogin">
      <aside class="sidebar">
          <el-menu default-active="/home" class="sidebar-menu" @select="handleMenuSelect">
              <el-menu-item index="/qagent/server">
                  <el-icon><ElIconCloudy /></el-icon>
                  <span>服务器引擎</span>
              </el-menu-item>
              <el-menu-item index="/qagent/server/container">
                  <el-icon><ElIconCpu /></el-icon>
                  <span>容器</span>
              </el-menu-item>
              <el-menu-item index="/docker/hub/images">
                  <el-icon><ElIconBox /></el-icon>
                  <span>镜像仓库</span>
              </el-menu-item>
              <el-menu-item index="/docker/hub/engine">
                  <el-icon><ElIconChromeFilled /></el-icon>
                  <span>hub-docker</span>
              </el-menu-item>
          </el-menu>
      </aside>
    </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import {ref, watch} from 'vue'
// 登录状态：从localStorage读取
const router = useRouter()
const route = useRoute()

const miniNav = ref(localStorage.getItem('miniNav') === 'true')

const handleMenuSelect = (path) => {
    router.push(path)
}
const isLogin = ref(false)
watch(
  () => route, // 监听当前路由的完整对象
  (newRoute, oldRoute) => {
     if (newRoute.path === '/login') {
        isLogin.value = false;
     } else {
        isLogin.value = true;
     }
  },
  {
    immediate: true,
    deep: true
  }
)

</script>

<style scoped>
.aside-menu {
    display: flex;
    width: 150px;
    background-color: #2c3e50;
    overflow-x: hidden;
    height: 100%;
    box-sizing: border-box;
}
.mini-menu {
    width: 40px;
}
.sidebar {
    color: #fff;
    height: 100%;
    padding-top: 20px;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #34495e;
}
.sidebar-menu {
    background-color: transparent !important;
    border-right: none !important;
}
.sidebar-menu .el-menu-item {
    color: #ecf0f1;
    height: 50px;
    line-height: 50px;
    padding-left: 10px !important;
}
.el-icon {
    margin-right: 10px !important;
}
.el-menu-item:hover {
    background-color: #2c3e5091;
    color: rgb(64 158 255);
}
</style>
