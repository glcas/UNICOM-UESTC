# 这个脚本应该放到任务计划，触发器设为“工作站锁定时” 尝试改代码为关机时运行，不再任务计划
# 需与logout脚本放在同一目录下
# 待调试的地方：登陆要求的是否是外网IP；cookie的传送已被忽略
# 最后打包成exe，打包前删除生成日志文件相关代码

import datetime
import socket

import requests


def main():
    log = open('log.txt', 'a')
    with open('Info.txt', 'r') as f:
        lines = f.readlines()
    JSESSIONID = lines[0][11:-2]
    CSRFToken = lines[1][10:-2]
    uuid = lines[2][5:-2]
    loggerID = lines[3][9:-2]
    try:
        logout = requests.get(
            'http://221.10.255.233:8088//LogoutServlet',
            params={
                'CSRFToken_HW': CSRFToken,
                'loggerId': loggerID,
                'wlanuserip': socket.gethostbyname(socket.gethostname()),
                'username': '02802118659',
                'wlanacname': 'pppoe',
                'ATTRIBUTE_UUID': uuid
            },
            headers={
                'Host': '221.10.255.233:8088',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept':'*/*',
                'Accept-Language':
                'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'http://221.10.255.233:8088//LoginServlet',
                'Cookie': 'JSESSIONID={}'.format(JSESSIONID)
            })
        log.write('{}'.format(datetime.datetime.now()))
        if logout.text == '[SUCCESS]':
            log.write('  logout success\n')
        else:
            log.write('  logout failed without request error\n')
    except requests.exceptions.RequestException:
        log.write('  logout failed\n')
    log.close()


if __name__ == "__main__":
    main()
