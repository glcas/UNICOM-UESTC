# 需与logout脚本放在同一目录下
# 最后打包成exe

from time import ctime, sleep

import pywifi
import requests
from ping3 import ping


def conwifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    inRegion = False
    for i in range(3):
        iface.scan()
        APList = iface.scan_results()
        for data in APList:
            if data.ssid == 'UNICOM-UESTC':
                inRegion = True
                break
        if inRegion is True:
            break
        sleep(10)
    if inRegion is False:
        return -1
    profile = pywifi.Profile()
    profile.ssid = 'UNICOM-UESTC'
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)
    temProfile = iface.add_network_profile(profile)
    for i in range(3):
        iface.connect(temProfile)
        sleep(3)
        for i in range(3):
            if iface.status() != pywifi.const.IFACE_CONNECTED:
                sleep(3)
            else:
                break
        if iface.status() == pywifi.const.IFACE_CONNECTED:
            break
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        return 0
    else:
        return -1


def connect(username, password):
    """ if first parameter==-1, the others is None, means that login failed """
    try:
        firstPage = requests.get(
            'http://221.10.255.233:8088/showlogin.do?ssid=pppoe',
            params={
                # wlanuserip': ip,
                # 'wlanacname': 'SCCD-CDZ-HW-ME60-B1',
                'ssid': 'pppoe'
            },
            headers={
                'Host': '221.10.255.233:8088',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'DNT': '1'
            },
            timeout=6)
        sleep(1)
        loggerID = firstPage.text[firstPage.text.index('logger') +
                                  36:firstPage.text.index('logger') + 53]
        CSRFToken = firstPage.text[firstPage.text.index('CSRFToken') +
                                   21:firstPage.text.index('CSRFToken') + 53]
        loginHeaders = {
            'Host': '221.10.255.233:8088',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://221.10.255.233:8088/showlogin.do?ssid=pppoe',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '481',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Origin': 'http://221.10.255.233:8088',
            'Cache-Control': 'max-age=0'
        }  # post head value
        loginPayload = {
            'username':
            username,
            'password':
            password,
            'loggerId':
            loggerID,
            'wlanuserip':
            firstPage.text[firstPage.text.index('wlanuserip') +
                           40:firstPage.text.index('wlanuserip') + 55],
            'wlanacname':
            '',
            'wlanmac':
            '',
            'firsturl':
            'http://www.baidu.com',
            'ssid':
            'pppoe',
            'userAgent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'usertype':
            'pc',
            'gotopage':
            '/GWlanRes/pppoe/LoginURL/pc/index.jsp',
            'successpage':
            '/GWlanRes/pppoe/OnlineURL/pc/index.jsp',
            'CSRFToken_HW':
            CSRFToken
        }
        loginPage = requests.post('http://221.10.255.233:8088//LoginServlet',
                                  headers=loginHeaders,
                                  data=loginPayload,
                                  timeout=6)
        sleep(1)
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
            f.write('{}  connect AP failed\n'.format(ctime()))
            break
        username, password = 'yourUsername', 'yourPassword'
        JSESSIONID, logoutUrl = connect(username, password)
        if JSESSIONID != -1:  # write the data to disk with no error
            f.write('{}  login success\n'.format(ctime()))
            with open('Info.txt', 'w') as f:
                f.write('JSESSIONID={}\n{}'.format(JSESSIONID, logoutUrl))
        while True:
            pingAns = defaultPing()
            if JSESSIONID == -1 and pingAns > 100:
                errTime += 1
                break
            if pingAns > 1000:
                errTime += 1
                break
            elif pingAns > 200:
                sleep(30)
            elif pingAns > 100:
                sleep(60)
            else:
                sleep(180)
        sleep(10)
        if errTime > 6:
            f.write('{}  with using Internet failed\n'.format(ctime()))
            break
    pywifi.PyWiFi().interfaces()[0].disconnect()


if __name__ == "__main__":
    main()
