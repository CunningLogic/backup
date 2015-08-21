#!/usr/local/bin/python
#-*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib
import urllib

#服务地址
host = "yunpian.com"
#端口号
port = 80
#版本号
version = "v1"
#查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
#通用短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
#模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"


apikey = "ea02074a60233f861a14ff1f7a57fe4a"
mobile = "18676783577"
text = "【大疆创新】#otter#同步数据延时为#latency#秒，最后同步时间为#last#!"
tpl_id = 840943

def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', user_get_uri + "?apikey=" + apikey)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_sms(apikey, text, mobile):
    """
    能用接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': tpl_value, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

if __name__ == '__main__':
    pass
    #apikey = "ea02074a60233f861a14ff1f7a57fe4a"
    #mobile = "18676783577,13928452841"
    #text = "【大疆创新】#otter#同步数据延时为#latency#秒，最后同步时间为#last#!"
    #查账户信息
    #print(get_user_info(apikey))
    #调用通用接口发短信
    #print(send_sms(apikey, text, mobile))
    #调用模板接口发短信
    #tpl_id = 840943 #对应的模板内容为：您的验证码是#code#【#company#】
    #tpl_value = '#code#=1234&#company#=云片网'
    #tpl_value = '#otter#=http://120.26.45.44:8080/&#latency#=30&#last#=2015-06-16 16:16:16'
    #print(tpl_send_sms(apikey, tpl_id, tpl_value, mobile))

