
from bubble.utils.logger import log
from bubble.utils.func import pack_res, save_file
from bubble.data.redis_con import rcon
from bubble.data.home import stock_pool, index_forecast, industry_forecast


from flask import Blueprint
home_bp = Blueprint('home', __name__, '/home')


@home_bp.route('/visit_counter', methods=['get', 'post'])
def visit_counter():
    r = rcon()
    r.incr('count', 1)
    count = int(r.get("count"))
    res = {'counter': f'{count}'}
    return pack_res(res)


@home_bp.route('/', methods=['get', 'post'])
def home_visit():
    res = {"stock_pool": stock_pool,
           "index_forecast": index_forecast,
           "industry_forecast": industry_forecast}
    return pack_res(res)