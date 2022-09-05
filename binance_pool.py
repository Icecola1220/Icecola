import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# import time  #用于对请求加延时，爬取速度太快容易被反爬
from time import sleep  # 同上
import time  # 用与获取实时时间

start_time = time.time()  # 程序开始时间
# 创建错误日志记录
logging.basicConfig(filename="Error.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.ERROR)

crawler_url = 'https://www.binance.com/zh-CN/swap/pool'  # 设置需要爬的链接
# 基本浏览器设置
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('--headless')  # 无头显示浏览器
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面


# 设置实例化浏览器，及设置

# txxt = ''  # 初始化，第一条对比文本
#txt = [1, 2, 3]
#txt_emoji = [1, 2, 3]
txt = ['','','','','','','','','','']
txt_emoji = ['','','','','','','','','','']
txt_def = []


def telegram_send(message):
    # Telegram_API链接信息配置
    bot_token = '5695810571:AAHUkIGjCwDMFQWLBzADRLN54IWqvtd2Kwg'  # Telegram_bot私钥
    bot_chatID = 'icecola_news'  # 频道名称
    #bot_token = '5321232286:AAGIDNJJZsSJrOFvuBR6tk3zMqn30_qagn0'  # Telegram_bot私钥
    #bot_chatID = 'icecola_new1'  # 频道名称
    # bot_message ="Testing"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=@' + bot_chatID + '&text=' + message
    # print(send_text)
    response = requests.get(send_text)  # 发送Telegram消息
    # print(response)


# 爬取币安poolTop10数据
def crawler():
    text = ""
    #browser = webdriver.Chrome("/Users/icecola/Documents/我的知识体系/Python改变世界/chromedriver", options=chrome_options)
    browser = webdriver.Chrome('/bin/chromedriver', options=chrome_options)  # linux运行地址
    browser.set_window_size(1440, 900)  # 设置屏幕大小，不同大小，展示样式都不同，需要注意
    # browser.maximize_window  #设置最大化浏览器

    browser.get(crawler_url)  # 打开要爬取的网页
    sleep(1)

    name = browser.find_element(By.XPATH,
                                "//*[@id='pool-container']/div[4]/div[1]/div/div[1]/div[1]/div[3]/div")  # 获取收益按钮
    # print(name.text)
    name.click()  # 排序，收益从高到低
    sleep(1)
    # 开始爬取数据从高到低
    # point = browser.find_element(By.XPATH, "//*[@id='pool-container']/div[4]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]")
    # print(point.text)
    # loct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #获取当前的实时时间
    # print(loct)

    for page in range(1, 11):  # 其实这个page是这个列表数据的列数。top10列

        # 这是币种信息
        page_name = f'//*[@id="pool-container"]/div[4]/div[1]/div/div[2]/div[{page}]/div/div[1]/div/div[1]/div/div/div[2]'
        # 这是流动性挖矿USDT
        # page_mint_value = f'//*[@id="pool-container"]/div[4]/div[1]/div/div[2]/div[{page}]/div/div[1]/div/div[2]/div/div[1]'
        # 这是收益率
        page_shouyi = f'//*[@id="pool-container"]/div[4]/div[1]/div/div[2]/div[{page}]/div/div[1]/div/div[3]/div/div[1]'
        # 这是交易量USDT
        # jiaoyiliang = f'//*[@id="pool-container"]/div[4]/div[1]/div/div[2]/div[{page}]/div/div[1]/div/div[5]/div'

        value_name = browser.find_element(By.XPATH, page_name).text  # 定位到的标签属性赋给point
        value_shouyi = browser.find_element(By.XPATH, page_shouyi).text  # 定位到的标签属性赋给point

        text = '第 ' + str(page) + ' 名:  ' + value_name + ' ' + value_shouyi + '\n'

        if txt[page - 1] == text:
            txt_emoji[page - 1] = text
        else:
            txt[page - 1] = text
            txt_emoji[page - 1] = '✅' + text
        # print(text)
        # point = browser.find_element(By.XPATH, page_mint_value) #流动性挖矿量
        # print(point.text)
        # point = browser.find_element(By.XPATH, page_shouyi)  #收益率
        # print(point.text)
        # point = browser.find_element(By.XPATH, jiaoyiliang)    #交易量
        # print(point.text)
    loct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end_time = time.time()
    end_time = (end_time - start_time) / 60
    print("耗时: {:.2f}分钟".format(end_time))
    #print(text)
    browser.quit()
    # return '第' + str(i) + '次' + ':' + loct + '\n' + text
    return txt, txt_emoji


if __name__ == "__main__":
    i = 0  # 循环数值
    while True:
        i += 1
        print('第', i, '次开始运行：')
        try:
            txt, txt_emoji = crawler()

            tt = "" #tt为循环，从列表中拉出文本
            if txt_def != txt:
                txt_def = txt
                for t in txt_emoji:
                    tt += t
                telegram_send(tt)
                #print("发送成功")
                #print(txt_emoji)
            else:
                #print("没有变化")
                pass

        except Exception as e:
            print('第', i, '次运行的错误')
            logging.exception(e)  # 捕获一个错误,并打印        continue
        # crawler()
        # telegram_send(str(i))
        print('第', i, '次结束')
        # sleep(10)

# 抓去一次binance数据，存入x；
# 拿到x推送到telegram
