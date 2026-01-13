import request from '@/utils/request'

export const registerAPI = {
    // 注册
    register: (data) => request.post('/api/auth/register', data)
}
