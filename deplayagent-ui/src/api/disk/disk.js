import request from '@/utils/request'

export const diskAPI = {
    // 扫描文件
    scan: (data) => request.post('/api/disk/dir/ref/manager/scan', data),
    getDir: (data) => {
        if (!data) {
            data = 0;
        }
        return request.post(`/api/disk/dir/ref/manager/getDir/${data}`);
    },
    outerDown: (urls) => request.post(`/api/disk/file/manager/outerDown`, {urls: [...urls]}, {
        timeout: 10 * 60 * 1000
    }),
    // 新增
    add: (data) => request.post('/api/disk/dir/ref/manager/add', data),
    update: (data) => request.post('/api/disk/dir/ref/manager/update', data),
    del: (data) => request.post('/api/disk/dir/ref/manager/del', data, {
        timeout: 60 * 1000
    }),
    updateAvatar: (data) => request.post('/api/disk/dir/ref/manager/update/avatar', data),
    spider: (data) => request.post('api/disk/dir/ref/manager/spider', data, {
        timeout: 10 * 60 * 1000
    }),
    getFileInfo: (id) =>request.post('/api/disk/dir/ref/manager/getInfo/'+id)
}
