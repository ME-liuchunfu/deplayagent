import request from '@/utils/request'

export const userAPI = {
    info: () => request.post('/api/auth/info'),
}
