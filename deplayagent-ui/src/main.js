import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/css/global.css' // 引入全局样式
import {requestEvents} from '@/events/requests-events'

// 引入Element Plus图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import dynamicRouter from "@/router/dynamic";
import {createPinia} from "pinia";

const pinia = createPinia();

const app = createApp(App)

// 全局注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(`ElIcon${key}`, component)
}

dynamicRouter.forEach(item=>{
    router.addRoute(item.name, item);
})


// ===================== 核心：配置全局定时器 =====================
// 定义变量存储定时器ID，全局唯一，方便后续清除
let globalTimer = null
// 多任务场景：定义对象存储多个定时器ID，key为任务名称，value为定时器ID
let globalTimerObj = {}

// 挂载全局定时器相关方法到 app.config.globalProperties
app.config.globalProperties.$timer = {
  // 1. 开启【单个全局定时器】- 常用
  // time: 间隔时间(毫秒)，callback: 定时器执行的回调函数
  start (time = 1000, callback) {
    // 开启前先清除，防止重复创建多个定时器叠加执行
    this.clear()
    globalTimer = setInterval(() => {
      callback && callback() // 执行自定义逻辑
    }, time)
  },

  // 2. 清除【单个全局定时器】
  clear () {
    if (globalTimer) {
      clearInterval(globalTimer)
      globalTimer = null // 清除后重置为null，释放内存
    }
  },

  // 3. 开启【多个全局定时器】- 多任务场景用（比如同时轮询接口A和接口B）
  // taskName: 任务名称(唯一标识)，time: 间隔时间，callback: 回调函数
  startTask (taskName, time = 1000, callback) {
    // 先清除当前任务的定时器，防止重复创建
    this.clearTask(taskName)
    globalTimerObj[taskName] = setInterval(() => {
      callback && callback()
    }, time)
  },

  // 4. 清除【单个指定任务】的定时器
  clearTask (taskName) {
    if (globalTimerObj[taskName]) {
      clearInterval(globalTimerObj[taskName])
      delete globalTimerObj[taskName] // 删除对象属性，释放内存
    }
  },

  // 5. 清除【所有全局定时器】- 退出登录/页面销毁时推荐调用
  clearAll () {
    this.clear() // 清除单定时器
    Object.keys(globalTimerObj).forEach(taskName => {
      this.clearTask(taskName) // 清除所有多任务定时器
    })
  }
}
requestEvents.install(router)
app.use(ElementPlus)
app.use(pinia)
app.use(router).mount('#app')
