import request from '@/utils/request'

export const fnFinanceInfoAPI = {
    list: (data) => request.post('/fn/finance/api/finance_info/list', data),
    add: (data) => request.post('/fn/finance/api/finance_info/add', data),
    update: (data) => request.post('/fn/finance/api/finance_info/update', data),
    delInfo: (data) => request.post('/fn/finance/api/finance_info/del', data),
}

export const fnFinanceCodeAPI = {
    list: (data) => request.post('/fn/finance/api/finance_code/list', data),
    add: (data) => request.post('/fn/finance/api/finance_code/add', data),
    update: (data) => request.post('/fn/finance/api/finance_code/update', data),
    delInfo: (data) => request.post('/fn/finance/api/finance_code/del', data),
}

export const fnFinanceCopiesAPI = {
    list: (data) => request.post('/fn/finance/api/finance_interest_copies/list', data),
    add: (data) => request.post('/fn/finance/api/finance_interest_copies/add', data),
    update: (data) => request.post('/fn/finance/api/finance_interest_copies/update', data),
    delInfo: (data) => request.post('/fn/finance/api/finance_interest_copies/del', data),
}
