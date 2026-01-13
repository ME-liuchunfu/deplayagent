import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/css/global.css' // 引入全局样式

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

app.use(ElementPlus)
app.use(pinia)
app.use(router).mount('#app')
