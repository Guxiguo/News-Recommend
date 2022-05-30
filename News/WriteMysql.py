import xlrd
import pymysql
# 第一步：打开文件
wb = xlrd.open_workbook('newsChinaDaily1.xls')
# 第二步：选取表单
sh = wb.sheet_by_name('新闻')
row = sh.nrows
print(row)
clo = sh.ncols
j = 1
conn = pymysql.connect(host='127.0.0.1',
                     user='guxiguo',
                     password='520134',
                     port=3306,
                     #db='student',
                     db='NewsRecommend',
                     charset='utf8')


for i in range(1, 4502):
    list = sh.row_values(i, 0, 6)
    news_link = "http:" + list[0]
    news_title = list[1]
    news_content = list[2]
    news_author = list[3]
    news_source = list[4]
    news_date = list[5]
    list.clear()
    if news_link != '' and news_title != '' and news_content != '' and news_author != '' and news_source != '':
        cur = conn.cursor()
        sql = "insert into News (news_id,news_title,news_content,news_link,news_author,news_source,news_date) values (%s,%s,%s,%s,%s,%s,%s);"
        data = (j, news_title, news_content, news_link, news_author, news_source, news_date)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        j = j+1

conn.close()
