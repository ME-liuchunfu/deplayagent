import {accountRouter} from "@/router/account";

const dynamicRouter = [
    {
        path: '/home',
        name: 'HomeView',
        component: ()=>import("@/views/layout/HomeView.vue"),
    },
    {
        path: '/qagent/server',
        name: 'QagentServer',
        component: ()=>import("@/views/qagent/QAgentServerView.vue"),
    },
    {
        path: '/docker/hub/engine',
        name: 'DockerHubEngine',
        component: ()=>import("@/views/docker/hub/DockerEngineView.vue"),
    },
    {
        path: '/docker/hub/images',
        name: 'DockerHubImages',
        component: ()=>import("@/views/docker/hub/DockerImagesView.vue"),
    },
    {
        path: '/qagent/server/container',
        name: 'QagentServerContainer',
        component: ()=>import("@/views/qagent/QAgentServerContainerView.vue"),
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