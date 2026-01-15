import {accountRouter} from "@/router/account";

const dynamicRouter = [
    {
        path: '/home',
        name: 'HomeView',
        component: ()=>import("@/views/layout/HomeView.vue"),
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFoundView',
        component: ()=>import("@/views/pages/NotFoundView.vue"),
        meta: { title: '页面不存在' }
    }
]

accountRouter.forEach(item=>dynamicRouter.push(item))

export default dynamicRouter