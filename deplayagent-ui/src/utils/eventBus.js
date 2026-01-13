// src/utils/eventBus.js
import mitt from 'mitt'

// 创建事件发射器实例
export const eventBus = mitt()

export const eventCi = (key, type, value) => {
    eventBus.emit(key, {
        type: type,
        value: value
    })
}

export const EVENT_KEYS = {
    REQUEST_KEY: 'EVENT:REQUEST:RESPONSE'
}