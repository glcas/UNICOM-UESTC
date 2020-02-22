# 需与login脚本放在同一目录下
# 最后打包成exe，打包前删除生成日志文件相关代码

from time import ctime
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
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept':
            '*/*',
            'Accept-Language':
            'zh-CN,zh;q=0.9',
            'Accept-Encoding':
            'gzip, deflate',
            'Connection':
            'keep-alive',
            'Referer':
            'http://221.10.255.233:8088//LoginServlet',
            'Cookie':
            'LOGIN_USER_NAME_COOKIE=02802118659; LOGIN_PASSWORD_COOKIE=184312; JSESSIONID={}'
            .format(JSESSIONID),
            'DNT':
            '1'
        }
        logout = requests.get(logoutUrl, headers=myHeaders)
        log.write('{}'.format(ctime()))
        if logout.text == '[SUCCESS]':
            log.write('  logout success\n')
        else:
            log.write('  logout failed without request error\n')
    except requests.exceptions.RequestException:
        log.write('{}  logout failed\n'.format(ctime()))
    finally:
        log.close()


if __name__ == "__main__":
    main()
