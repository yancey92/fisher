"""
 health check
"""
from flask import make_response, current_app
from flask import jsonify
from . import web


@web.route("/hello")
def hello():
    # 其实返回的是一个元组
    # return "Hello",200,headers={}
    return jsonify("Hello 杨欣")


def test_response():
    """测试 response, 并重定向"""
    headers = {
        # Content-Type 指定客户端接收到响应后，如何解释响应的内容
        "Content-Type": "application/json",
        "location": "https://baidu.com",
    }
    response = make_response("hello!", 301)
    response.headers = headers
    return response


"""
    add_url_rule 是 Flask 中用于动态添加路由规则的方法
    下面的 add_url_rule 也可以写成这样的：web.add_url_rule(rule="/test/", endpoint='test_response')
"""
web.add_url_rule(rule="/test/", view_func=test_response)
