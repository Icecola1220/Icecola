import pymysql
from telegram_send import telegram_send

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='icecola@123', db='kol', charset='utf8mb4')
#linux数据库地址
#db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='icecola', db='kol', charset='utf8mb4')


def insertDB(Table_loct, Table_name, Table_username, Table_desc, Table_followers):
    # 插入数据
    try:
        Table_name = Table_name.replace('"', "'")
        Table_desc = Table_desc.replace('"', "'")
        sql = 'insert into twitter_kol_1 values ("%s","%s","%s","%s","%s")' % (
            Table_username, Table_followers, Table_loct, Table_name, Table_desc)
        db.cursor().execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        #print(Table_loct, '\n', Table_name, '\n', Table_username, '\n', Table_desc, '\n', Table_followers, '\n', '\n')
        #msg = "Table_loct, '\n', Table_name, '\n', Table_username, '\n', Table_desc, '\n', Table_followers, '\n', '\n'"
        #telegram_send(msg)


# a = '2022-09-12 15:32:10 '
# b = ' /s"陳威廉 '
# c = ' William11Chan '
# d = 'The leading DEX Aggregator, offering the best swap returns across 17 chains. Join us: https://t.co/SK3ljHPZkk'
# e = ' 110798 '
#
# insertDB(a,b,c,d,e)
