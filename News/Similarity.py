
import xlrd
import jieba
import pymysql

#打开停用词表，返回一个停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('D:/NewsRecommend/News/stop_words.txt', encoding='UTF-8').readlines()]
    return stopwords


#连接MySQL数据库并且查询news表中的news_content内容
def connect_Mysql():
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    sql = "select news_content from News;"
    cur = conn.cursor()
    cur.execute(sql)
    list = cur.fetchall()
    cur.close()
    conn.close()
    return list

#对新闻内容进行分词
#sentence是新闻内容
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    #print("正在分词")
    str=''.join(sentence)
    sentence_depart = jieba.cut(str, cut_all=False)
    #print(sentence_depart)
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ()
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += (word,)
                #outstr += " "
    return outstr

#读取情感词典文件中的内容，返回字典
#excel是文件名称
def ReadWord(excle):
    wb = xlrd.open_workbook(excle)
    # 第二步：选取表单
    sh = wb.sheet_by_name('Sheet1')
    row = sh.nrows
    #print(row)
    clo = sh.ncols
    #print(clo)
    dict = {}
    for i in range(1, 114768):
        list = sh.row_values(i, 0, 2)
        word = list[0]
        score = list[1]
        list.clear()
        dict[word] = score
    return dict
#读取否定词
def ReadPrivate(excel):
     wb = xlrd.open_workbook(excel)
     # 第二步：选取表单
     sh = wb.sheet_by_name('Sheet1')
     #row = sh.nrows
     list = sh.col_values(0)
     list.pop(0)
     return list

#读取程度词
def ReadMost(excel):
    wb = xlrd.open_workbook(excel)
    # 第二步：选取表单
    sh = wb.sheet_by_name('Sheet1')
    most_dic = {}
    for i in range(1, sh.nrows):
        list = sh.row_values(i, 0, 2)
        most_dic[list[0]] = list[1]
    return most_dic





#计算相似度
#杰卡迪尔相似系数
#line1,line2分别是两个比较的分词后的集合
def Similarity(line1, line2):
    sum1 = 0
    list1 = list(set(line1+line2))
    len1 = len(list1)
    for word in line1:
        if word in line2:
            sum1 = sum1 + 1
    if sum1 != 0:
        simil = sum1/len1
    else:
        simil = 0
    return simil

#插入情感得分到数据库
def Insert_Mysql(news_id1, news_id2, similarity):
    '''conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()'''
    sql = "insert into Similarity (news_id1,news_id2,similarity) values (%s,%s,%s);"
    data = (news_id1, news_id2, similarity)
    cur.execute(sql, data)
    conn.commit()
    '''cur.close()
    conn.close()'''


lists = connect_Mysql()
print(lists[640])
print(len(lists))

conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
cur = conn.cursor()
dicc = ReadWord('D:/NewsRecommend/News/BosonNLP_sentiment_score.xls')
most_dic = ReadMost('D:/NewsRecommend/News/most.xlsx')
private = ReadPrivate('D:/NewsRecommend/News/privative.xlsx')
simil = 0
news_id1 = 639
news_id2 = 639
for line1 in lists[639]:
    news_id1 = news_id1+1
    for line2 in (lists[news_id1:4239]):
        #print(lists[news_id1], lists[4239])
        news_id2 = news_id2+1
        if line1 != line2:
            print(line1, line2)
            result1 = seg_depart(line1)
            result2 = seg_depart(line2)
            simil = Similarity(result1, result2)

        if simil != 0:
            print(simil, news_id1, news_id2)
            Insert_Mysql(news_id1, news_id2, simil)
        if news_id2 == 4239:
            news_id2 = news_id1
cur.close()
conn.close()

    #d = Classify(dicc, result)
    #s = TotalScore(dicc,  result)
    #s = socre_sentiment(dicc, private, most_dic, result)
    #Update_Mysql(s, news_id)
    #news_id += 1
    #print(d, s)
