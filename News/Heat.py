import datetime

import pymysql


def Connect_Mysql(news_id):
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    sql = "select news_date, news_scan, news_comment from News where news_id=%s;"
    cur = conn.cursor()
    cur.execute(sql, news_id)
    list = cur.fetchall()
    cur.close()
    conn.close()
    return list


def heat(scan, comment, date):
    a = datetime.date.today()
    day = (a - date).days
    return scan*0.4+comment*0.5-day*0.1


def Write_Mysql(news_id, heat):
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = "update newsparticiple set heat = %s where news_id = %s"
    data = (heat, news_id)
    cur.execute(sql, data)
    conn.commit()
    cur.close()
    conn.close()


for i in range(1, 4240):
    list = Connect_Mysql(i)
    print(list)
    date = list[0][0]
    scan = list[0][1]
    comment = list[0][2]
    print(scan, comment, date)
    score = heat(scan, comment, date)
    Write_Mysql(i, score)
    print(score)

