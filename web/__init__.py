
def resp_ok(data=None, msg="操作成功"):
    """成功响应"""
    return {"code": 200, "msg": msg, "data": data}


def resp_fail(msg="操作失败", code=400):
    """失败响应"""
    return {"code": code, "msg": msg, "data": None}