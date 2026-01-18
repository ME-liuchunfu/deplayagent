import request from '@/utils/request'

export const serverApi = {
    list: (query) => request.get('/api/qagent/server/list', {params: query}),
    listids: () => request.get('/api/qagent/server/ids'),
    get: (id) => request.get('/api/qagent/server/get/'+id),
    add: (data) => request.post('/api/qagent/server/add', data),
    put: (data) => request.post('/api/qagent/server/put', data),
    del: (data) => request.post('/api/qagent/server/del', data)
}
