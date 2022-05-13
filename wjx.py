import requests
import random
import re
import time
import threading

def get_response(url, header):
    response = requests.get(url=url, headers=header, verify=False)
    return response

def get_jqnonce(response):
    jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', response.text)
    return jqnonce.group()

def get_rn(response):
    """
    通过正则表达式找出rn,rn是构造post_url需要的参数
    :param response: 访问问卷网页，返回的reaponse
    :return: 找到的rn
    """
    rn = re.search(r'\d{9,10}\.\d{8}', response.text)
    return rn.group()

def get_id(response):
    """
    通过正则表达式找出问卷id,问卷是构造post_url需要的参数
    :param response: 访问问卷网页，返回的reaponse
    :return: 找到的问卷id
    """
    id = re.search(r'\d{8}', response.text)
    return id.group()

def get_jqsign(ktimes, jqnonce):
    """
    通过ktimes和jqnonce计算jqsign,jqsign是构造post_url需要的参数
    :param ktimes: ktimes
    :param jqnonce: jqnonce
    :return: 生成的jqsign
    """
    result = []
    b = ktimes % 10
    if b == 0:
        b = 1
    for char in list(jqnonce):
        f = ord(char) ^ b
        result.append(chr(f))
    return ''.join(result)

def get_start_time(response):
    """
        通过正则表达式找出问卷starttime,问卷是构造post_url需要的参数
        :param response: 访问问卷网页，返回的reaponse
        :return: 找到的starttime
    """
    start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}', response.text)
    return start_time.group()

def set_header(ip):
    """
    随机生成ip，设置X-Forwarded-For
    ip需要控制ip段，不然生成的大部分是国外的
    :return:
    """
    header = {
        'X-Forwarded-For': ip,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
                    ) Chrome/71.0.3578.98 Safari/537.36',
        }
    return header

def get_ktimes():
    """
    随机生成一个ktimes,ktimes是构造post_url需要的参数，为一个整数
    :return:
    """
    return random.randint(5, 18)


def set_post_url(url, ip):
    """
    生成post_url
    :return:
    """
    header = set_header(ip)  # 设置请求头，更换ip
    response = get_response(url, header)  # 访问问卷网页，获取response
    ktimes = get_ktimes()  # 获取ktimes
    jqnonce = get_jqnonce(response)  # 获取jqnonce
    rn = get_rn(response)  # 获取rn
    id = get_id(response)  # 获取问卷id
    jqsign = get_jqsign(ktimes, jqnonce)  # 生成jqsign
    start_time = get_start_time(response)  # 获取starttime
    time_stamp = '{}{}'.format(int(time.time()), random.randint(100, 200))  # 生成一个时间戳，最后三位为随机数
    post_url = 'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttime={}&ktimes={}&rn={}&jqnonce={}&jqsign={}'.format(id, time_stamp, start_time, ktimes, rn, jqnonce,jqsign)
    print(post_url)
    return post_url


def main(URL, data):
    ip = '{}.{}.{}.{}'.format(112, random.randint(64, 68), random.randint(0, 255), random.randint(0, 255))
    print(ip)
    url = set_post_url(URL, ip)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4'
                      '044.129 Safari/537.36 Edg/81.0.416.68',
        'Referer': URL,
        'Origin': 'www.wjx.com',
        'Connection': 'close',
        'Host': 'www.wjx.cn',
        'X-Forwarded-For': ip,
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6',
        'Content - Type': 'application / x - www - form - urlencoded'
    }

    print(data)
    r = requests.post(url, data=data, headers=header, verify=False)
    print(r)
    print(r.text)

if __name__ == '__main__':
    NUM = "0000000"
    URL = f'https://www.wjx.cn/jq/{NUM}.aspx'
    
    for i in range(100):
        # data = {
        # 'submitdata': '1$1}2$1}3$}4$%s}5$3}6$2}7$2}8$1}9$}10$1!%s,2!%s}11$}12$}13$' % (
        # str(random.randint(1, 2)), str(random.randint(1, 5)), str(random.randint(1, 5)))}


        data = {'submitdata': '1$2}2$1}3$2'}
        t = threading.Thread(target=main, args=(URL, data))
        t.start()