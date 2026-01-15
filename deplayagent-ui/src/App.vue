<template>
    <div class="app-container">
      <!-- 侧边栏 -->
      <aside-menu class="aside" />
      <!-- 主内容区 -->
      <main class="main-content">
          <top-nav />
          <router-view />
      </main>
    </div>
</template>

<script setup>
import TopNav from "@/views/layout/TopNav.vue";
import AsideMenu from "@/views/layout/AsideMenu.vue";

</script>

<style scoped>
/* 保持原样式不变 */
#app {
  font-family: 'Segoe UI', sans-serif;
  height: 100vh;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
}
.app-container {
  display: flex;
  height: 100%;
}
.main-content {
    flex: 1;
}
.aside {
  height: 100vh;
}
</style>