import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='icecola@123', db='icecola', charset='utf8')


def insertDB(datetime, paiming, tokenid, nianhua, mint_value, jiaoyiliang):
    # 插入数据
    try:
        sql = "insert into mytable values ('%s','%s','%s','%s','%s','%s')" % (datetime, paiming, tokenid, nianhua, mint_value, jiaoyiliang)
        db.cursor().execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
