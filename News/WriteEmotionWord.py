
import xlrd
import pymysql
# 第一步：打开文件
wb = xlrd.open_workbook('D:/NewsRecommend/News/BosonNLP_sentiment_score.xls')
# 第二步：选取表单
sh = wb.sheet_by_name('Sheet1')
row = sh.nrows
print(row)
clo = sh.ncols
print(clo)
conn = pymysql.connect(host='127.0.0.1',
                     user='guxiguo',
                     password='520134',
                     port=3306,
                     #db='student',
                     db='NewsRecommend',
                     charset='utf8')


for i in range(1, 114768):
    list = sh.row_values(i, 0, 2)
    word = list[0]
    score = list[1]
    print(list)
    list.clear()
    cur = conn.cursor()
   
    sql = "insert into bosonnlp (word, score) values (%s,%s);"
    data = (word, score)
    cur.execute(sql, data)
    conn.commit()
    cur.close()

conn.close()