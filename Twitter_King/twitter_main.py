import json
import re
import time
from selenium.webdriver.chrome.service import Service
from db_twitter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 变量区#
TIMEOUT = 10  ### 测试的时候，各个地方的timeout可以设置的小一点，在实际程序运行的时候需要设置的更大一点
userID_list = [ ]  # 创建推特User列表
baseUrl = 'https://www.twitter.com'  # 访问网址
start = time.time()


# 基础的浏览器配置信息，并加载cookie并隐藏浏览器信息登录推特页面
def init(url):
    cookieFile = '/Users/icecola/Desktop/twitterCookie.json'
    stealthFile = '/Users/icecola/Desktop/stealth.min.js'
    # cookie文件
    with open(cookieFile, 'r') as f:
        cookie = json.load(f)
    # 隐藏浏览器的文件
    with open(stealthFile) as f:
        js = f.read()
    # 开始浏览器的基础配置
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    chromeOptions.add_argument("--proxy-server=http://127.0.0.1:7890")  # 添加本地代理
    chromeOptions.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chromeOptions.add_argument('--headless')  # 无头显示浏览器
    chromeOptions.add_argument('--disable-gpu')  # 禁用GPU图像加速
    chromeOptions.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chromeOptions.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # 这个吊毛方法是开启性能日志，默认状态是关闭，输出getlog是‘brower’日志，开启后输出性能日志，re少不了他
    capabilities = DesiredCapabilities.CHROME
    capabilities[ 'goog:loggingPrefs' ] = {"performance": "ALL"}  # newer: goog:loggingPrefs
    # 开始正式装载进浏览器驱动中。。。
    s = Service("/Users/icecola/Documents/我的知识体系/Python改变世界/chromedriver")
    driver = webdriver.Chrome(service=s,
                              options=chromeOptions, desired_capabilities=capabilities)
    # 隐藏浏览器指纹信息
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    print('Chrome基本配置已完成')
    # 开始访问推特，未响应则返回超时异常
    while True:
        try:
            driver.get(url)
            sleep(3)
            driver.save_screenshot('/Users/icecola/Desktop/1.png')
            break
        except:
            sleep(TIMEOUT // 10)
    # 读取cookie并加载进浏览器，进行真实用户登录（免登录过程）
    for item in cookie:
        item.pop("sameSite")
        driver.add_cookie(item)
    driver.get(url)
    sleep(3)
    driver.save_screenshot('/Users/icecola/Desktop/2.png')
    print('携cookie已经登录成功！！！并进入到起始用户推特主页面')
    return driver


# 登陆个人推特主界面，并抛出个人的基本信息，name, uid, intro, followingNum
def getUserInfo(driver, userPageUrl):
    driver.get(userPageUrl)  # 进入个人推特主界面
    nameXpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[1]/span'
    uidXpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div/span'
    introXpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/div/span'
    followingNumXpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div[5]/div[1]/a/span[1]/span'
    # print(driver.page_source)
    print('开始抓取起始用户的数据')
    # 判断是否获取name值，初始化超时为10秒，10秒内正常进行，超过10秒抛出异常
    name = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, nameXpath))).text  # 每0.5秒检查until里面的元素是否获取，如果获取则进行下一步
    print('数据抓取成功')
    uid = driver.find_element(By.XPATH, uidXpath).text
    # 为了防止有些人介绍信息为空异常，加入Try函数
    try:
        intro = driver.find_element(By.XPATH, introXpath).text
    except:
        intro = ''
    # 对主动关注的人数进行拆分
    try:
        followingNum = int(
            driver.find_element(By.XPATH, followingNumXpath).text.replace(',', '').replace('.', '').replace('K', '000'))
    except:
        followingNum = 1000  # 如果为整数则为1000
    # 输出，并返回基本信息
    print('输出首发用户信息： ', '  |  ', name, '  |  ', str(uid), '  |  ', intro, '  |  ', followingNum, '  |  ')
    return uid


# 进入到个人Following主动关注的KOL推特页面，持续录入这些KOL的基本信息，最终输出Following数量
def getFollowing(driver, userid):
    userFollowingPageUrl = baseUrl + '/' + userid + '/following'
    driver.get(userFollowingPageUrl)  # 打开推特following页面
    sleep(TIMEOUT // 10)
    scrollUntilLoaded(driver)  # 这是持续滑动到底部的方法。到底后自动结束break
    # 将推特的name信息复制给targetUserName
    getuid = userid
    sleep(TIMEOUT // 10)
    # 先将following页面全部滚完，然后，最后统一收集整理日志信息。
    # 这一行就牛逼了，先查看浏览器后台日志，找到对应的用户日志后并通过json解析，最终返回主动关注的推特KOL数量
    getFollowingResponse(getuid, driver)


# 这是一个，调用就持续往下滑动的方法，一直滑到最底部才结束break
def scrollUntilLoaded(driver):
    # 先获取现有的底部坐标信息，并赋值给last_height
    last_height = driver.execute_script("return document.body.scrollHeight")
    # print('获取底部信息：', last_height)
    page = 0
    max_page = 30  # 最大往下滚动扒拉读取页数
    print('正在获取Following页数：')
    while page < max_page:  # 页数太多，内存爆掉
        # 执行将页面滑动到底部坐标的js操作。
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(TIMEOUT // 6)
        # 执行结束之后，页面加载出新的页面，然后重新获得底部坐标，然后赋值new_height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # print('获取新的底部信息：', new_height)
        # 持续往下滑动
        page += 1  # 页数
        print(page, end=' ')
        if new_height == last_height:
            break
        last_height = new_height


# 此为核心关键程序代码！！！！
# 查看浏览器后台日志，筛选出推特用户的response文件，并json解码，摘出用户信息，录入list，最后抛出主动关注的推特KOL数量
def getFollowingResponse(getuid, driver):
    print('\n持续解码中，数据正在录入ing...')
    for row in driver.get_log('performance'):  # 获取后台输出的所有日志
        log_data = row
        # 读取浏览器后台的日志[message]里的信息
        log_json = json.loads(log_data[ 'message' ])
        log = log_json[ 'message' ]
        # 匹配对应可以获取用户信息的Following的日志文件
        if log[ 'method' ] == 'Network.responseReceived' and 'Following' in log[ 'params' ][ 'response' ][ 'url' ]:
            # 找到对应的requestId，每一个http请求，都有一个id，通过id，可以直接获取response
            requestId = log[ 'params' ][ 'requestId' ]
            try:
                # cdp为谷歌开发者协议，execute_cdp_cmd调用谷歌协议用的，根据requestid获得了response的json内容，爬虫的最爱
                responseBody = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": requestId})[ 'body' ]
                # print(responseBody)
                # 将获得json给解码，仅仅一行，读了1小时源码，2022年09月14日。
                decodeFollowingReponse(responseBody)
            except Exception as e:
                print('本次录入失败')
                print(e)
                pass
    print('当前已完成录入', len(uidlistDB()), '人')


# 解析FollowingResponse的，解析完将用户信息存入list，并最后抛出这一页的推特用户数量
def decodeFollowingReponse(responseBody):
    user_list = [ ]  # 装载每次解码的数据list
    responseBody = json.loads(responseBody)
    allInstructions = responseBody[ 'data' ][ 'user' ][ 'result' ][ 'timeline' ][ 'timeline' ][ 'instructions' ]
    # 找到藏着推特用户数据的entries列表
    for instruction in allInstructions:
        if instruction[ 'type' ] == 'TimelineAddEntries':
            allEntries = instruction[ 'entries' ]
            break
    for ids in range(len(allEntries) - 2):  # 每次都会多两个，最后两个是我们不需要的
        result = allEntries[ ids ][ 'content' ][ 'itemContent' ][ 'user_results' ][ 'result' ]
        if result.get('legacy'):
            userContent = result[ 'legacy' ]
            name = userContent[ 'name' ]  # 获取网名
            intro = userContent[ 'description' ]  # 获取推特介绍
            uid = userContent[ 'screen_name' ]  # 获取推特id
            followers_count = userContent[ 'followers_count' ]  # 获取该推特用户的粉丝数
            friends_count = userContent[ 'friends_count' ]  # 获取该用户主动关注的数量
            user_list.append([ uid, name, friends_count, followers_count, intro ])
    #print(user_list)
    userRule(user_list)  # 进入规则筛选阶段，并发送数据库，和续上Userid


#   增加re语言识别，判定是否为中文kol
def userRule(userinfo_list):
    # user_list[uid,name,主动关注数，粉丝数，info]
    # list[45, '隔壁老王', 2, 900, '你好im a bot上の取扱']
    # 遍历list中的userinfo信息，粉丝低于1000,pass
    userRule_list = [ x for x in userinfo_list if x[ 3 ] > 100 ]
    # 去重录入，需要联系数据库，这里写错了，先注释掉
    # userRule_list = list(set([tuple(i) for i in userRule_list]))
    # 根据粉丝数量来从大到小排序
    userRule_list = sorted(userRule_list, key=lambda x: x[ 3 ], reverse=True)
    # print(userRule_list)
    # 如果中文字符在字符串中数量最多，则判断为中文，同时保留其他主要语种
    count_jp = count_cn = count_en = count_ko = count_other = 0
    jp = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')  # 匹配为日文
    ko = re.compile(r'[\uAC00-\uD7A3]')  # 匹配韩文
    cn = re.compile(r'[\u4e00-\u9fa5]')  # 匹配中文
    en = re.compile(r'[a-zA-z]')  # 匹配英文
    # 统计list中的info介绍字符串语言信息：
    for u in userRule_list:
        ii = u[4]
        # print(ii)
        if jp.search(ii):
            count_jp += 1
        elif cn.search(ii):
            count_cn += 1
        elif en.search(ii):
            count_en += 1
        elif ko.search(ii):
            count_ko += 1
        else:
            count_other += 1
        # 根据统计的不同语言字符数量，对list进行插入语言种类
        # ("uid","推特名称","主动关注数","粉丝数","是否中文","个人简介")
        if max(count_jp, count_cn, count_en, count_ko) == count_cn and count_cn > 0:
            u.insert(4, 'CN')
            insertDB(u[0], u[1], u[2], u[3], u[4], u[5])
        elif max(count_jp, count_cn, count_en, count_ko) == count_en and count_cn > 0:
            u.insert(4, 'EN')
            insertDB(u[0], u[1], u[2], u[3], u[4], u[5])
        elif max(count_jp, count_cn, count_en, count_ko) == count_jp and count_cn > 0:
            u.insert(4, 'JP')
            insertDB(u[0], u[1], u[2], u[3], u[4], u[5])
        elif max(count_jp, count_cn, count_en, count_ko) == count_ko and count_cn > 0:
            u.insert(4, 'KO')
            insertDB(u[0], u[1], u[2], u[3], u[4], u[5])
        else:
            u.insert(4, 'Unknown')
            insertDB(u[0], u[1], u[2], u[3], u[4], u[5])


if __name__ == '__main__':
    # 基本的浏览器环境配置，开启性能日志，加载cookie。隐藏浏览器指纹。等等均在此
    driver = init(baseUrl)
    # 录入第一个首发用户id
    startUserUrl = baseUrl + '/' + 'icecola1220'
    # 展示起始用户的基本信息情况
    # userID_list.append(getUserInfo(driver, startUserUrl))

    userID_list = ['icecola1220']
    #print(userID_list)
    # 获取第一个推特用户的主页信息，[name, uid, intro, followingNum]，
    # sys.exit(0)
    # 这一段，直接三个函数（拉浏览器后台日志、json解码，持续滑动页面）被拉起，最后返回该用户主动关注的推特KOL数量
    # startUserFollowerNum = getFollowing(driver, userID_list[0])  # 引入的info的用户列表
    # 开始循环拉取following列表，并持续将UID加入到list里面

    #########################################
    # 如果中断，请从此开始操作，手动录入userid！！
    userID_list += uidlistDB()
    print('数据库已录入： ', len(userID_list))
    #########################################
    i = 1618
    while i < 5000:
        i += 1
        try:
            userID_list += uidlistDB()
            print(f'\n\n------------当前进入第{i}轮------------')
            UserUrl = baseUrl + '/' + str(userID_list[i-1])
            #print(UserUrl)
            #driver = init(UserUrl)
            getFollowing(driver, userID_list[i-1])  # 引入的info的用户列表
            print(f'-----已完成第{i}轮录入,累计', len(uidlistDB()), '人-----')
            end = time.time()
            runtime = end - start
            print('累计已经运行时间: %d 分 %d 秒' % (runtime // 60, runtime % 60))
            # driver.close()
            # driver.quit()
        except:
            # 遇错则关闭所有浏览器，重启载入
            driver.close()
            driver.quit()
            UserUrl = baseUrl + '/' + userID_list[i-1]
            driver = init(UserUrl)
