import request from '@/utils/request'

export const imagesApi = {
    list: (hubId) => request.get('/api/hub/docker/registry/repositories/all/'+hubId),
    del: (data) => request.post('/api/hub/docker/registry/repositories/del', data)
}
