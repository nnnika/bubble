code, start, end, fields(e.g.收盘价)
table 在路径上

json形式
get和post方法参数获取
flask路径变量获取 前端往后端传参数

# get和post
1. get请求：
        使用场景：如果只对服务器获取数据，并没有对服务器产生任何影响，那么这时候使用get请求
        传参：get请求传参是放在url中，并且是通过？的形式来指定key和value的
2. post请求：
        使用场景：如果要对服务器产生影响，那么使用post请求
        传参：post请求传参不是放在URL中，是通过form data 的形式发送给服务器的
* get 其他年轻是通过flask.request.args来获取
* post请求是通过flask.request.form来获取
* post请求在模板中要注意几点:
    * input 标签中，要写name来表示这个value的key,方便后台获取
    * 在写form表单的时候，要指定method=‘post’,并且要指定action='/login/'  
    


