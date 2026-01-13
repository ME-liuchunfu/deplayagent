import axios from 'axios'
import { ElMessage } from 'element-plus'
import cacheInfo from "@/stores/cacheInfo";
import {eventCi, EVENT_KEYS} from "@/utils/eventBus";

console.log('当前环境：', process.env.NODE_ENV)
console.log('API基础路径：', process.env.VUE_APP_BASE_API)

// 创建 axios 实例
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API, // 基础URL（从环境变量读取）
    timeout: 5000, // 超时时间
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
})

// 请求拦截器
service.interceptors.request.use(
    (config) => {
        let token = cacheInfo.token();
        if (token) {
            const tokenValue = token['tokenValue'];
            const tokenName = token['tokenName'];
            config.headers[tokenName] = tokenValue
        }
        return config
    },
    (error) => {
        ElMessage.error('请求参数错误')
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    (response) => {
        const res = response.data;
        eventCi(EVENT_KEYS.REQUEST_KEY, 'R_OK', res)
        // 成功返回数据
        return res.data
    },
    (error) => {
        // HTTP状态码处理
        eventCi(EVENT_KEYS.REQUEST_KEY, 'R_ERROR', error.response)
        return Promise.reject(error)
    }
)

export default service
