import pymysql

# from telegram_send import telegram_send

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='icecola@123', db='icecola', charset='utf8mb4')


# linux数据库地址
# db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='icecola', db='kol', charset='utf8mb4')
# 这个是查询函数，返回数据库里的uid
def uidlistDB():
    cs1 = db.cursor()
    sql1 = "SELECT uid FROM  twitter_cn"
    cs1.execute(sql1)
    datalist = []
    alldata = cs1.fetchall()
    for s in alldata:
        datalist.append(s[0])
    return datalist


def insertDB(Table_0, Table_1, Table_2, Table_3, Table_4, Table_5):
    # 插入数据
    try:
        Table_1 = Table_1.replace('"', "'")  # 对单双引号进行转换
        Table_5 = Table_5.replace('"', "'")

        if Table_4 == 'CN':
            sql = 'insert into twitter_cn values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                Table_0, Table_1, Table_2, Table_3, Table_4, Table_5)
        elif Table_4 == 'EN':
            sql = 'insert into twitter_en values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                Table_0, Table_1, Table_2, Table_3, Table_4, Table_5)
        elif Table_4 == 'JP':
            sql = 'insert into twitter_jp values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                Table_0, Table_1, Table_2, Table_3, Table_4, Table_5)
        elif Table_4 == 'KO':
            sql = 'insert into twitter_ko values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                Table_0, Table_1, Table_2, Table_3, Table_4, Table_5)
        elif Table_4 == 'Unknown':
            sql = 'insert into twitter_other values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                Table_0, Table_1, Table_2, Table_3, Table_4, Table_5)
        db.cursor().execute(sql)
        db.commit()

    except Exception as e:
        db.rollback()
        print(str(e))


# ("uid","推特名称","主动关注数","粉丝数","是否中文","个人简介")
# a = 111
# b = ' 陳威廉 '
# c = 123
# d = 110798
# f = 'FALSE'
# e = 'The leading DEX Aggregator, offering the best swap returns across 17 chains. Join us: https://t.co/SK3ljHPZkk'
#
# # sql = "insert into color(url, time) values('%s','%s')" % (Url，Time)
# aa = [a, b, c, f, d, e]
# insertDB(aa)
