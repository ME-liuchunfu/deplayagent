<template>
    <div class="aside-menu" :class="{'mini-menu': miniNav}">
      <aside class="sidebar">
          <el-menu default-active="/disk" class="sidebar-menu" @select="handleMenuSelect">
              <el-menu-item index="/shared">
                  <el-icon><ElIconShare /></el-icon>
                  <span>云服务器</span>
              </el-menu-item>
              <el-menu-item index="/favorites">
                  <el-icon><Star /></el-icon>
                  <span>收藏夹</span>
              </el-menu-item>
          </el-menu>
      </aside>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {ref} from 'vue'
// 登录状态：从localStorage读取
const router = useRouter()

const miniNav = ref(localStorage.getItem('miniNav') === 'true')

const handleMenuSelect = (path) => {
    router.push(path)
}

</script>

<style scoped>
.aside-menu {
    display: flex;
    width: 150px;
    background-color: #2c3e50;
    overflow: hidden;
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
