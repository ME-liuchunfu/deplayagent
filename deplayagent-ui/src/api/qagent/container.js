import request from '@/utils/request'

export const containerApi = {
    list: (query) => request.get('/api/qagent/server_container/list', {params: query}),
    token: () => request.post('/api/qagent/server_container/token'),
    rollback: (id, data) => request.post('/api/qagent/server_container/rollback/'+id, data),
    syncdata: (token) => request.post('/api/qagent/server_container/sync?token='+token, {}, {
        timeout: 60 * 1000
    }),
    up: (id) => request.post('/api/qagent/server_container/up/'+id),
    down: (id) => request.post('/api/qagent/server_container/down/'+id),
    restart: (id) => request.post('/api/qagent/server_container/restart/'+id)
}
