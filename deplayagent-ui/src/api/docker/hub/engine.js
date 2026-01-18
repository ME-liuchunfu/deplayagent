import request from '@/utils/request'

export const engineApi = {
    list: (query) => request.get('/api/hub/docker/machine/list', {params: query}),
    listids: () => request.get('/api/hub/docker/machine/ids'),
    get: (id) => request.get('/api/hub/docker/machine/get/'+id),
    add: (data) => request.post('/api/hub/docker/machine/add', data),
    put: (data) => request.post('/api/hub/docker/machine/put', data),
    del: (data) => request.post('/api/hub/docker/machine/del', data)
}
