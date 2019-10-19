# 需与login脚本放在同一目录下
# 最后打包成exe，打包前删除生成日志文件相关代码

import time
import requests


def main():
    with open('Info.txt', 'r') as f:
        lines = f.readlines()
    JSESSIONID = lines[0][11:-1]
    logoutUrl = lines[-1]
    log = open('log.txt', 'a')
    try:
        myHeaders = {
            'Host':
            '221.10.255.233:8088',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Accept':
            '*/*',
            'Accept-Language':
            'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':
            'gzip, deflate',
            'Connection':
            'keep-alive',
            'Referer':
            'http://221.10.255.233:8088//LoginServlet',
            'Cookie':
            'JSESSIONID={}; LOGIN_USER_NAME_COOKIE=02802118659; LOGIN_PASSWORD_COOKIE=184312'
            .format(JSESSIONID)
        }
        logout = requests.get(logoutUrl, headers=myHeaders)
        log.write('{}'.format(time.ctime()))
        if logout.text == '[SUCCESS]':
            log.write('  logout success\n')
        else:
            log.write('  logout failed without request error\n')
    except requests.exceptions.RequestException:
        log.write('{}  logout failed\n'.format(time.ctime()))
    finally:
        log.close()


if __name__ == "__main__":
    main()
