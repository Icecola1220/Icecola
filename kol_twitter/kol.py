import sys
import requests
import time  # 用与获取实时时间
from db_kol import insertDB
from telegram_send import telegram_send
from time import sleep

proxy = {'https_proxy': 'http://127.0.0.1:7890', 'http_proxy': 'http://127.0.0.1:7890','all_proxy': 'socks5://127.0.0.1:7890'}

# 伪装请求头，避免反爬
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


# 使用requests.get()方法获取网页返回数据，并使用循环更改url的page_start参数
def crawler(i):
    # 将"？"前的部分url提取出来
    url = 'https://twitterscan.com/appapi/twitter-scan/trading-kol-v2'
    # 封装字典网址请求参数
    param = {'category': 'project',
             'page_num': str(i),
             'page_size': '20'}
    response = requests.get(url, params=param, headers=headers,proxies=proxy)
    #response = requests.get(url, params=param, headers=headers)
    # 使用json方法，将获取到的字符串数据转换为字典/列表
    js_web = response.json()
    # 逐层展开字典，获取电影列表
    list_web = js_web['data']['records']
    # 循环遍历列表，获取每个电影的信息
    loct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取当前的实时时间
    if list_web:
        for kol in list_web:
            name = kol['name']
            username = kol['username']
            desc = kol['desc']
            followers = str(kol['followers'])
            #print(loct, name, username, desc, followers)
            insertDB(loct, name, username, desc, followers)
    else:
        print('已全部加载完毕,程序自动结束')
        end_time = time.time()
        end_time = end_time - start_time
        print("耗时: {:.2f}秒".format(end_time))
        #telegram_send('已全部加载完毕,程序自动结束'+"耗时: {:.2f}秒".format(end_time))
        sys.exit(0)


if __name__ == "__main__":
    start_time = time.time()  # 程序开始时间
    t = 0  # 循环数值
    while t < 10000:
        t += 1
        try:
            crawler(t)
            #sleep(0.1)
            print(f'第{t}次完成')
        except Exception as e:
            print(f'第{t}次运行出错了！！！！！！！','\n','正在重新执行',f'第{t}次')
            #telegram_send(f"第{t}次运行出错了")
            crawler(t)
            print(f'第{t}次完成')


