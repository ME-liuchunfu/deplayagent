import { createRouter, createWebHistory } from 'vue-router'
import cacheInfo from "@/stores/cacheInfo";
import LoginView from '@/views/account/LoginView.vue'


const routes = [
    {
        path: '/',
        redirect: '/home' // 默认跳转到首页
    },
    {
        path: '/login',
        name: 'LoginView',
        component: LoginView,
        meta: {
            ignore: true
        }
    }
]


const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    // scrollBehavior() {
    //     return { top: 0 } // 路由切换时滚动到顶部
    // }
})

// 路由守卫：未登录访问"我的"页面时跳转到登录页
router.beforeEach((to, from, next) => {
    if (to.meta['ignore'] !== true && !cacheInfo.isLogin()) {
        next('/login')
    } else {
        next()
    }
})

export default router
