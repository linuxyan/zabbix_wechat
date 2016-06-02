#!/usr/bin/python
#coding=utf-8
__author__ = 'Yan'

import urllib2,json

def GetToken(CorpID,Secret):
    tokenurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' %(CorpID,Secret)
    response = urllib2.urlopen(tokenurl)
    html = response.read().strip()
    ret = json.loads(html)
    if 'errcode' in ret.keys():
        print ret['errmsg']
        return 'Error'
    access_token = ret['access_token']
    return access_token

def GetUserInfo(Token):
    userurl = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=%s&department_id=1&fetch_child=1&status=1' %Token
    response = urllib2.urlopen(userurl)
    html = response.read().strip()
    ret = json.loads(html)
    if ret['errmsg'] == 'ok':
        userlist_info = ret['userlist']
        return userlist_info
    else:
        return "ERROR"

def SendMessage(Token,message,department,AgentID):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' %Token
    values = {
       "touser": "",
       "toparty": department,
       "totag": "",
       "msgtype": "text",
       "agentid": AgentID,
       "text": {
           "content": message
       },
       "safe":"0"
    }
    print values
    data = json.dumps(values,ensure_ascii=False)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req)
    result = response.read().strip()
    print result
    result = json.loads(result)
    if result['errmsg'] == 'ok':
        return 'ok'
    else:
        return 'Error'

if __name__ == '__main__':
    pass

