# 这个脚本应该放到任务计划，触发器设为登陆时，条件为停止现有实例；考虑是否勾选“只有在以下网络可用时启动”之选项？
# 运行逻辑：每一次登陆windows账号时登陆WiFi，锁定时下线
# 需与logout脚本放在同一目录下
# 最后打包成exe

import socket
import time

import pywifi
import requests
from ping3 import ping


def conwifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    inRegion = False
    while iface.status() == pywifi.const.IFACE_INACTIVE:
        time.sleep(1)
    for i in range(3):
        iface.scan()
        while iface.status() == pywifi.const.IFACE_SCANNING:
            time.sleep(0.5)
        APList = iface.scan_results()
        for data in APList:
            if data.ssid == 'UNICOM-UESTC':
                inRegion = True
                break
        if inRegion is True:
            break
        time.sleep(10)
    if inRegion is False:
        return -1
    profile = pywifi.Profile()
    profile.ssid = 'UNICOM-UESTC'
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)
    temProfile = iface.add_network_profile(profile)
    iface.connect(temProfile)
    while iface.status() == pywifi.const.IFACE_DISCONNECTED:
        time.sleep(1)
    if iface.status() == pywifi.const.IFACE_DISCONNECTED:
        for i in range(3):
            time.sleep(3)
            iface.connect(temProfile)
            while iface.status() == pywifi.const.IFACE_CONNECTING:
                time.sleep(1)
            if iface.status() == pywifi.const.IFACE_DISCONNECTED:
                continue
            if iface.status() == pywifi.const.IFACE_CONNECTED:
                return 0
        return -1
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        return 0
    else:
        return -1


def connect(ip, username, password):
    """ if first parameter==-1, the others is None, means that login failed """
    try:
        firstPage = requests.get(
            'http://221.10.255.233:8088/showlogin.do',
            params={
                'wlanuserip': ip,
                'wlanacname': 'SCCD-CDZ-HW-ME60-B1',
                'ssid': 'pppoe'
            },
            headers={
                'Host': '221.10.255.233:8088',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':
                'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            },
            timeout=6)
        loggerID = firstPage.text[firstPage.text.index('logger') +
                                  36:firstPage.text.index('logger') + 53]
        CSRFToken = firstPage.text[firstPage.text.index('CSRFToken') +
                                   21:firstPage.text.index('CSRFToken') + 53]
        loginHeaders = {
            'Host':
            '221.10.255.233:8088',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':
            'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':
            'gzip, deflate',
            'Referer':
            'http://221.10.255.233:8088/showlogin.do?wlanuserip={}&wlanacname=SCCD-CDZ-HW-ME60-B1&ssid=pppoe'
            .format(ip),
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Content-Length':
            '460',
            'Connection':
            'keep-alive',
            'Upgrade-Insecure-Requests':
            '1'
        }  # post head value
        loginPayload = {
            'username': username,
            'password': password,
            'loggerId': loggerID,
            'wlanuserip': ip,
            'wlanacname': 'SCCD-CDZ-HW-ME60-B1',
            'wlanmac': '',
            'firsturl': 'http://www.baidu.com',
            'ssid': 'pppoe',
            'userAgent':
            'Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64;+rv:67.0)+Gecko/20100101+Firefox/67.0',
            'usertype': 'pc',
            'gotopage': '/GWlanRes/pppoe/LoginURL/pc/index.jsp',
            'successpage': '/GWlanRes/pppoe/OnlineURL/pc/index.jsp',
            'CSRFToken_HW': CSRFToken
        }
        loginPage = requests.post('http://221.10.255.233:8088//LoginServlet',
                                  headers=loginHeaders,
                                  data=loginPayload,
                                  timeout=6)
        JSESSIONID = loginPage.headers['Set-Cookie'].split('=')[1][:-6]
        uuid = loginPage.text[loginPage.text.index('UUID') +
                              5:loginPage.text.index('UUID') + 37]
        logoutUrl = loginPage.text[loginPage.text.index('gurl') +
                                   8:loginPage.text.index('gurl') +
                                   187] + '&ATTRIBUTE_UUID=' + uuid
        return JSESSIONID, logoutUrl
    except requests.exceptions.RequestException:
        return -1, None


def defaultPing():
    """ always return ms """
    sum, n = 0, 6
    for website in ('bilibili.com', 'zhihu.com', 'baidu.com', 'qq.com',
                    'jd.com', 'uestc.edu.cn'):
        temp = ping(website, unit='ms')
        if temp is None:
            n -= 1
        else:
            sum += temp
    if n == 0:
        return 4000
    else:
        return sum / n


def main():
    while True:
        err = conwifi()
        errTime = 0
        f = open('log.txt', 'a')
        if err == -1:
            f.write('{}  connect AP failed\n'.format(time.ctime()))
            break
        ip = socket.gethostbyname(socket.gethostname())
        username, password = '02802118659', '184312'
        JSESSIONID, logoutUrl = connect(ip, username, password)
        if JSESSIONID != -1:  # write the data to disk with no error
            f.write('{}  login success\n'.format(time.ctime()))
            with open('Info.txt', 'w') as f:
                f.write('JSESSIONID={}\n{}'.format(JSESSIONID, logoutUrl))
        while True:
            if JSESSIONID == -1:
                errTime += 1
                break
            pingAns = defaultPing()
            if pingAns > 1000:
                errTime += 1
                break
            elif pingAns > 200:
                time.sleep(30)
            elif pingAns > 100:
                time.sleep(60)
            else:
                time.sleep(180)
        time.sleep(10)
        if errTime > 6:
            f.write('{}  with using Internet failed\n'.format(time.ctime()))
            break
    pywifi.PyWiFi().interfaces()[0].disconnect()


if __name__ == "__main__":
    main()
