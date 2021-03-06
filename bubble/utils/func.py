import json



def pack_res(res, code=200, msg="success"):
    res = {
        "data": res,
        "code": code,
        "msg": msg
    }
    return json.dumps(res, ensure_ascii=False)


def save_file(file, file_path):
    with open(file_path, "wb") as f:
        f.write(file)