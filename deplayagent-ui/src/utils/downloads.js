import request from "@/utils/request";



export const downloads = {
    getBaseUrl: () =>{
        const config = localStorage.getItem("disk-server-config")
        if (config) {
            const dict = JSON.parse(config)
            return dict['url']
        }
        return null;
    },
    tokens: async () => {
        const url = await request.get('/api/disk/file/manager/token')
        return url;
    },
    joinUrl: (url, uri) => {
        if (uri.startsWith("/") && url.endsWith("/")) {
            uri = uri.substring(1, uri.length)
            return url + uri;
        } else if (uri.startsWith("/") || url.endsWith("/")) {
            return url + uri;
        }
        return url + "/" + uri;
    },
    getDownTokeUrl: async (uri) => {
        if (!uri) {
            return null;
        }
        const url = await downloads.tokens()
        return downloads.joinUrl(url, uri);
    },
    down: async (url, fileName) => {
        try {
            // 1. 发起 fetch 请求（支持携带 Token 等请求头）
            const response = await fetch(url);
            // 3. 将响应转换为 Blob 对象（二进制数据）
            const blob = await response.blob();
            // 4. 从响应头中获取文件名（可选，需后端配合）
            // const contentDisposition = response.headers.get('Content-Disposition');
            // if (contentDisposition) {
            //     // 解析 Content-Disposition 中的文件名（兼容不同格式）
            //     const match = contentDisposition.match(/filename="?(.+?)"?$/);
            //     if (match && match[1]) {
            //         fileName = decodeURIComponent(match[1]); // 解码特殊字符
            //     }
            // }
            // 5. 创建临时 URL 并触发下载
            const blobUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = blobUrl;
            a.download = fileName; // 指定下载文件名
            a.click(); // 触发下载

            // 6. 释放临时 URL（重要：避免内存泄漏）
            URL.revokeObjectURL(blobUrl);
        } catch (error) {
            console.error('下载失败：', error);
        }
    },
    blobData: async (url) => {
        try {
            // 1. 发起 fetch 请求（支持携带 Token 等请求头）
            const response = await fetch(url);
            // 3. 将响应转换为 Blob 对象（二进制数据）
            const blob = await response.blob();
            return blob;
        } catch (error) {
            console.error('下载失败：', error);
        }
        return null;
    },
}
