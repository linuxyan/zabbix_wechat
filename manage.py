#!/usr/bin/python
#coding=utf-8

from flask import Flask,request
import sys
from WXBizMsgCrypt import WXBizMsgCrypt
from wechat import GetToken, GetUserInfo ,SendMessage
import xml.etree.cElementTree as ET

app = Flask(__name__)
sToken = "CoKy9XHn"
sEncodingAESKey = "gGfhnbHN8bllFyc7tLcv3vCXNvSlJEiANRxiG65jTkE"
sCorpID = "wx9b32a4b30268070a"
Secret='ZL74qB4Jd2L5fAC8lP4LdtXrshKj-vwCeWMawRSJjgKz00Gg_OGRsfhduNxo_4Ho'

@app.route('/', methods=['GET','POST'])
def hello_world():
    sVerifyMsgSig = request.args.get('msg_signature')
    sVerifyTimeStamp = request.args.get('timestamp')
    sVerifyNonce = request.args.get('nonce')
    wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
    sVerifyMsgSig=sVerifyMsgSig
    sVerifyTimeStamp=sVerifyTimeStamp
    sVerifyNonce=sVerifyNonce
    if request.method == 'GET':
        sVerifyEchoStr = request.args.get('echostr')
        if sVerifyEchoStr != 'None':
           sVerifyEchoStr=sVerifyEchoStr
           ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
           if(ret!=0):
              print "ERR: VerifyURL ret: " + ret
              sys.exit(1)
           return sEchoStr
        else:
            return ''
    elif request.method == 'POST':
        sReqData = request.data
        ret,sMsg=wxcpt.DecryptMsg( sReqData, sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce)
        if( ret!=0 ):
            print "ERR: DecryptMsg ret: " + ret
            sys.exit(1)
        #print sMsg
        xml_tree = ET.fromstring(sMsg)
        FromUserName = xml_tree.find("FromUserName").text
        AgentID = xml_tree.find("AgentID").text
        EventKey = xml_tree.find("EventKey").text
        Token = GetToken(sCorpID,Secret)
        userlist = GetUserInfo(Token)
        if userlist == 'ERROR':
            print 'Get User Info failed!'
        for userdict in userlist:
            if userdict['userid'] == FromUserName:
                name = userdict['name']
                department_id = userdict['department'][0]
        if EventKey == 'accept':
            message = u'%s 接手处理!' %name
        elif EventKey == 'end':
            message = u'%s 处理完成!' %name

        message = message.encode("utf8")
        result = SendMessage(Token,message,department_id,AgentID)
        if not result == 'ok':
            print "Send Message failed"
        return 'Post Success!'

if __name__ == '__main__':
    app.run(debug=True)
