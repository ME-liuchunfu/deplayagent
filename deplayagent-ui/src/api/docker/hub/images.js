import request from '@/utils/request'

export const imagesApi = {
    list: (hubId) => request.get('/api/hub/docker/registry/repositories/all/'+hubId),
    del: (data) => request.post('/api/hub/docker/registry/repositories/del', data),
    query: (hub_id) => request.get('/api/hub/docker/registry/repositories/query/'+hub_id),
    tags: (hub_id, repo) => request.get('/api/hub/docker/registry/repositories/tags/'+hub_id+"?repo="+repo),
}
