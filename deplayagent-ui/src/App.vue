<template>
    <div class="app-container">
      <!-- 侧边栏 -->
      <aside-menu/>
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
import { getCurrentInstance, onUnmounted } from 'vue'
import cacheInfo from "@/stores/cacheInfo";
import {authAPI} from "@/api/login";

const { proxy } = getCurrentInstance()

proxy.$timer.start(10000, async () => {
  console.log('flush', new Date().getTime())
  if (!cacheInfo.isLogin()) {
      return;
  }
  try{
     const now = new Date().getTime()
     const token = cacheInfo.token()
     let expires_minutes = token.expires_minutes
     let mul = token.now
     let tm = 60 * 1000 * expires_minutes + mul
     if (tm > now + 5 * 60 * 1000) {
        console.log('at time:' + now)
        return
     }
     const res = await authAPI.reflush();
     console.log(res)
     if (res && res['access_token']) {
        cacheInfo.setLogin(res)
     }
  } catch(_) {
     console.error(_)
  }
})

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
  flex: 1;
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100vh;
}
.main-content {
    flex: 1;
    overflow: scroll;
}
</style>