import RegisterView from "@/views/account/RegisterView.vue";
import ForgetPasswdView from "@/views/account/ForgetPasswdView.vue";

export const accountRouter = [
    {
        path: '/register',
        name: 'RegisterView',
        component: RegisterView,
        meta: {
            ignore: true
        }
    },
    {
        path: '/forget-passwd',
        name: 'ForgetPasswdView',
        component: ForgetPasswdView,
        meta: {
            ignore: true
        }
    }
]
