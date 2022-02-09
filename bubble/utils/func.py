import json
"""
code

200  成功

"""


def pack_res(res, code=200, msg="success"):
    res = {
        "data": res,
        "code": code,
        "msg": msg
    }
    return json.dumps(res, ensure_ascii=False)