import requests
import json
import socket
import time
import re
import sys
import hashlib

# 校园网账号
userid = "账号"
# 校园网密码
passwd = "密码"
# 校园网管理后台登录域名
xywhost = "http://11.11.11.11"
# 校园网登录链接的wlanacname
wlanacname = "XXXX"

hostsname = socket.gethostname()
loginmsg = "test"

#       主程序
def main():
    # try:
        global passmd5
        passmd5 = get_md5(passwd)
        print("*******程序开始运行*******","\n主机名：",hostsname,"\n你的IP是:", ip())
        print("3秒后开始登录操作")
        time.sleep(2)
        logout()
        login()
    # except:
        print("")
        exit

#       获取内网IP
def ip():
    global ip
    global passmd5
    url = "http://1.1.1.1"
    x = requests
    r = x.get(url, allow_redirects=False)
    rtext = r.text
    result = re.search(r"\d{1,3}.\d{2,3}.\d{1,3}.\d{1,3}",str(rtext))
    ip = result.group()
    return ip

def login():
    global ip
    #       登录操作
    x2 = requests
    x = requests.session()
    x.get(xywhost)
    quickAuthShare = x.get(xywhost + "/quickAuthShare.do?wlanacip=&wlanacname=" + wlanacname + "&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=" + ip)
    data = json.loads(quickAuthShare.text)
    loginmsg = data["message"]
    #       获取验证码
    r = x.post(xywhost + "/self/tologin.do")
    data = json.loads(r.text)
    verifyCode = data["data"]["verifyCode"]
    print("验证码:",verifyCode)
    #       登录操作获取cookie
    headers={
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': xywhost,
    'Referer': xywhost + '/self/index.html',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    data = '{"accountId":"' + userid + '","password":"' + passmd5 + '","verifyCode":"'
    r2 = x.post(url=xywhost + "/self/login.do?",headers=headers,data=data+verifyCode+"\"}")
    data = json.loads(r2.text)
    status = data["errmsg"]
    print("登录:",status)
    print(loginmsg)

    #       数据变量
    num = 0
    times = 0
    while True:
        try:
            #       获取在线清单和设备ID
            data2 = '{"accountId":"' + userid + '"}'
            r3 = x.post(url=xywhost +"/self/getonline.do?",headers=headers,data=data2)
            data = json.loads(r3.text)
            online = data["rows"]
            if('billingId'in r3.text):
                print("**********设备在线*******")
                online = data["rows"][0]["billingId"]
                serverIp = data["rows"][0]["serverIp"]
                ip = data["rows"][0]["accountIp"]
                print("在线设备：",online,"\n设备IP：",ip,)
            #       下线设备
                data3 = '{"accountId":"' +userid + '","accountIp":"'+ ip +'","billingId":"'+ online +'","serverIp":"' + serverIp + '"}'
                r4 = x.post(url=xywhost+"/self/kickonline.do?",headers=headers,data=data3)
                quickAuthShare = x.get(xywhost + "/quickAuthShare.do?wlanacip=&wlanacname="+ wlanacname + "&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=" + ip)
                data = json.loads(r4.text)
                status = data["errmsg"]
                times += 1
                print("设备" + status  + "，拨号" + str(times) + "次")
                num = 0
                time.sleep(1)
                quickAuthShare = x.get(xywhost + "/quickAuthShare.do?wlanacip=&wlanacname="+ wlanacname + "&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=" + ip)
                data = json.loads(quickAuthShare.text)
                loginmsg = data["message"]
                print(loginmsg)

            else:
                num += 1
                if ( num>5 ):
                    headers2={
                    'Cache-Control': 'no-cache'
                    }
                    r5 = x2.get("http://h5.analytics.126.net/news/c", headers=headers2 , allow_redirects=False)
                    if( 'ok'in r5.text ):
                        print("登录状态：联网成功！")
                        print("登录状态：联网成功！")
                        print("登录状态：联网成功！")
                        exit()
                    else:
                        print("登录状态：登录失败！")
                        logout()
                        login()  
                else:
                    pass
                    time.sleep(1)
        except:
                print("")
                break
def logout():
    #       断网操作
    x = requests.session()
    r = x.get(xywhost+"/quickAuthShare.do?wlanacip=&wlanacname="+ wlanacname +"&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=" + ip)
    data = json.loads(r.text)
    distoken = data["distoken"]
    print("distoken:",distoken)
    time.sleep(2)
    r2 = x.get(xywhost+"/httpservice/appoffline.do?wlanacip=&wlanacname="+ wlanacname +"&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=&distoken="+ distoken)
    data = json.loads(r2.text)
    message = data["message"]
    print("下线状态:",message)
    quickAuthShare = x.get(xywhost + "/quickAuthShare.do?wlanacip=&wlanacname="+ wlanacname +"&userId=" + userid + "&passwd=" + passwd + "&mac=&wlanuserip=" + ip)


def get_md5(v):
    import hashlib
    # Message Digest Algorithm MD5（中文名为消息摘要算法第五版）为计算机安全领域广泛使用的一种散列函数，用以提供消息的完整性保护
    md5 = hashlib.md5()   #md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
    ## update需要一个bytes格式参数
    md5.update(v.encode('utf-8'))  #要对哪个字符串进行加密，就放这里
    value = md5.hexdigest()  #拿到加密字符串
    return value


main();
