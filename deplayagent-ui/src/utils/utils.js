import {ElMessage} from "element-plus";

export const commonUtil = {
    copyTest: async (text)=>{
        try {
            await navigator.clipboard.writeText(String(text))
            ElMessage.success('复制成功 ✔️')
          } catch (err) {
            ElMessage.error('复制失败 ❌，请手动复制')
            console.error('复制报错：', err)
          }
    },
    inArray: (arr, item) => {
        for (let k in arr) {
            if (arr[k] && arr[k] === item) {
                return true;
            }
        }
        return false;
    },
    toDataString: (data) =>{
        if (data instanceof String) {
            return data;
        }
        try {
            return JSON.stringify(data);
        } catch (e) {
            return data.toString();
        }
    },
    parseJson(value) {
        try {
            return JSON.parse(value);
        } catch (_) {
            return value;
        }
    },
    /**
     * 判断函数是否为 async 函数
     * @param {Function} fn - 待判断的函数
     * @returns {boolean} 是否为 async 函数
     */
    isAsyncFunction: (fn) => {
        // 先确保是函数（避免非函数参数报错）
        if (typeof fn !== 'function') return false;
        // async 函数的 toString 结果为 "[object AsyncFunction]"
        return Object.prototype.toString.call(fn) === '[object AsyncFunction]';
    },
    /**
     * 自动执行普通函数或 async 函数（非 async 环境可用）
     * @param {Function} fn - 待执行的函数（普通函数/async 函数）
     * @param {any[]} args - 函数参数（可选）
     * @param {Object} options - 配置项（可选）
     * @param {Function} options.onSuccess - 成功回调
     * @param {Function} options.onError - 错误回调
     */
    executeFunction: (fn, args = [], { onSuccess, onError } = {}) => {
        if (typeof fn !== 'function') {
            onError?.('传入的不是函数');
            return;
        }

        try {
            // 执行函数，获取返回值（普通函数返回结果，async 函数返回 Promise）
            const result = fn(...args);

            // 判断是否为 async 函数（通过返回值是否为 Promise 辅助确认，更严谨）
            if (commonUtil.isAsyncFunction(fn) || result instanceof Promise) {
                // 处理 async 函数（Promise 结果）
                result
                    .then((res) => onSuccess?.(res))
                    .catch((err) => onError?.(err instanceof Error ? err.message : err));
            } else {
                // 处理普通函数（直接返回结果）
                onSuccess?.(result);
            }
        } catch (err) {
            // 捕获普通函数的同步错误（如 fn 执行时抛错）
            onError?.(err instanceof Error ? err.message : err);
        }
    }
}
