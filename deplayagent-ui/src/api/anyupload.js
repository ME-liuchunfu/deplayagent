import request from '@/utils/request'

export const anyUploadAPI = {
    // 扫描文件
    upload: async (file, onUploadProgress) => {
        const formData = new FormData();
        formData.append('file', file);
        return request.post('/api/disk/file/manager/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            timeout: 60 * 60 * 1000,
            onUploadProgress: (progressEvent) => {
                onUploadProgress && onUploadProgress.call(this, progressEvent);
            }
        });
    },

}
