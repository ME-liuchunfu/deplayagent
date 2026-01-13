// 格式化文件大小
export const formatFileSize1 = (bytes) => {
    if (!bytes || bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 获取文件类型
export const getFileType = (mimeType) => {
    if (!mimeType) return 'other'
    if (mimeType.startsWith('image/')) return 'image'
    if (mimeType.startsWith('video/')) return 'video'
    if (mimeType.startsWith('audio/')) return 'audio'
    if (mimeType.startsWith('text/') ||
        ['application/json', 'application/javascript', 'text/plain'].includes(mimeType)) {
        return 'text'
    }
    return 'other'
}

// 格式化时间（时间戳 → yyyy-MM-dd hh:mm）
export const formatTime = (timestamp) => {
    if (!timestamp) return 'unknown'
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:${minute}`;
};

// 格式化时间（时间戳 → yyyy-MM-dd）
export const formatDate = (timestamp) => {
    if (!timestamp) return 'unknown'
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

// 格式化文件大小（B → KB/MB/GB）
export const formatFileSize = (size) => {
    if (!size) return '0B';
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    if (size < 1024 * 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    return `${(size / (1024 * 1024 * 1024)).toFixed(1)} GB`;
};

// 根据文件名获取对应图标组件（Element Plus Icons）
export const fileIconComponent = (fileName) => {
    let suffix = fileName;
    if (fileName) {
        suffix = fileName.split('.').pop().toLowerCase();
    }
    const iconMap = {
        pdf: 'Reading',
        doc: 'Reading',
        docx: 'Reading',
        xls: 'Reading',
        xlsx: 'Reading',
        ppt: 'Reading',
        pptx: 'Reading',
        jpg: 'PictureFilled',
        jpeg: 'PictureFilled',
        png: 'PictureFilled',
        gif: 'PictureFilled',
        mp4: 'VideoPlay',
        mov: 'VideoPlay',
        mp3: 'Mic',
        wav: 'Mic',
        txt: 'Document',
    };
    const icon = iconMap[suffix] || "File";
    return `ElIcon${icon}` // 默认图标
};
