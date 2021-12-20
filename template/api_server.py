from flask import Flask
from flask import request
import json


server = Flask(__name__)


# 接口：http://192.168.199.163:8888/login?pwd=111&name=xiaoshi
@server.route('/login',methods=['get','post'])
def login():
    #获取通过url请求传参的数据
    username = request.values.get('name')
    #获取url请求传的密码，明文　
    pwd=request.values.get('pwd')
    #判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if username and pwd:
        if username == 'xiaoshi' and pwd == '111':
            resu={'code':200,'message':'登录成功'}
            return json.dumps(resu,ensure_ascii=False)#将字典转换为Json串，json是字符串
        else:
            resu={'code':-1,'message':'账号密码错误'}
            return json.dumps(resu,ensure_ascii=False)

    else:
        resu={'code':1001,'message':'参数不能为空'}
        return json.dumps(resu,ensure_ascii=False)


if __name__== '__main__':
    server.run(debug=True,port = 8888,host='0.0.0.0')