import json
import requests
import socket


def proxy():
    # 请求地址
    try:
        targetUrl = 'http://ip123.in/ip.json'
        ip = 'oracle.accessconnect.cc'
        proxy = {'https_proxy': ip, 'http_proxy': ip}
        resp = requests.get(targetUrl, proxies=proxy)
        # print(resp.status_code)
        ip = json.loads(resp.text)
        txt = ip['ip']  # + ' ' + ip['country_code']
        print(txt)
    except:
        txt = '网络异常'
        print(txt)
    return txt

proxy()


def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'http')
    print(myaddr[0][4][0])


getIP('oracle.accessconnect.cc')
#'183.2.197.108'
#183.2.197.139
#183.2.204.185
