import redis


def rcon():
    r = redis.Redis(host='wallyi.com', port=6380, db=0)
    return r
