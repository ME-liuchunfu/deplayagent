import request from '@/utils/request'

export const userAPI = {
    // 扫描文件
    info: () => request.post('/api/auth/info'),
}
